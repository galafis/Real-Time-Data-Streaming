#!/usr/bin/env python3
"""
Real-Time Data Streaming
Apache Kafka-like streaming data processing system with Python.
"""

import json
import time
import threading
import queue
import logging
from datetime import datetime
from typing import Dict, List, Any, Callable
from dataclasses import dataclass
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template_string
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class StreamMessage:
    """Data structure for streaming messages."""
    topic: str
    key: str
    value: Dict[str, Any]
    timestamp: datetime
    partition: int = 0

class StreamProducer:
    """Produces messages to streaming topics."""
    
    def __init__(self, broker: 'StreamBroker'):
        self.broker = broker
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def send(self, topic: str, key: str, value: Dict[str, Any]) -> bool:
        """Send message to topic."""
        try:
            message = StreamMessage(
                topic=topic,
                key=key,
                value=value,
                timestamp=datetime.now()
            )
            return self.broker.publish(message)
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False
    
    def send_batch(self, topic: str, messages: List[Dict[str, Any]]) -> int:
        """Send batch of messages."""
        sent_count = 0
        for i, msg in enumerate(messages):
            if self.send(topic, f"key_{i}", msg):
                sent_count += 1
        return sent_count

class StreamConsumer:
    """Consumes messages from streaming topics."""
    
    def __init__(self, broker: 'StreamBroker', group_id: str):
        self.broker = broker
        self.group_id = group_id
        self.subscribed_topics = set()
        self.running = False
        self.message_handler = None
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def subscribe(self, topics: List[str]):
        """Subscribe to topics."""
        self.subscribed_topics.update(topics)
        for topic in topics:
            self.broker.add_consumer(topic, self)
        self.logger.info(f"Subscribed to topics: {topics}")
    
    def set_message_handler(self, handler: Callable[[StreamMessage], None]):
        """Set message processing handler."""
        self.message_handler = handler
    
    def start_consuming(self):
        """Start consuming messages."""
        self.running = True
        self.logger.info("Started consuming messages")
        
        while self.running:
            try:
                for topic in self.subscribed_topics:
                    messages = self.broker.consume(topic, self.group_id)
                    for message in messages:
                        if self.message_handler:
                            self.message_handler(message)
                time.sleep(0.1)  # Small delay to prevent busy waiting
            except Exception as e:
                self.logger.error(f"Error consuming messages: {e}")
    
    def stop_consuming(self):
        """Stop consuming messages."""
        self.running = False
        self.logger.info("Stopped consuming messages")

class StreamBroker:
    """Simple in-memory message broker."""
    
    def __init__(self):
        self.topics = {}
        self.consumers = {}
        self.message_queues = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def create_topic(self, topic: str, partitions: int = 1):
        """Create a new topic."""
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = {
                    'partitions': partitions,
                    'messages': [[] for _ in range(partitions)]
                }
                self.consumers[topic] = []
                self.logger.info(f"Created topic: {topic} with {partitions} partitions")
    
    def publish(self, message: StreamMessage) -> bool:
        """Publish message to topic."""
        try:
            with self.lock:
                if message.topic not in self.topics:
                    self.create_topic(message.topic)
                
                # Simple partitioning by hash of key
                partition = hash(message.key) % self.topics[message.topic]['partitions']
                message.partition = partition
                
                self.topics[message.topic]['messages'][partition].append(message)
                self.logger.debug(f"Published message to {message.topic}:{partition}")
                return True
        except Exception as e:
            self.logger.error(f"Error publishing message: {e}")
            return False
    
    def consume(self, topic: str, group_id: str, max_messages: int = 10) -> List[StreamMessage]:
        """Consume messages from topic."""
        messages = []
        try:
            with self.lock:
                if topic in self.topics:
                    for partition_messages in self.topics[topic]['messages']:
                        if partition_messages:
                            # Simple consumption - take from beginning
                            consumed = partition_messages[:max_messages]
                            messages.extend(consumed)
                            # Remove consumed messages
                            del partition_messages[:len(consumed)]
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e}")
        
        return messages
    
    def add_consumer(self, topic: str, consumer: StreamConsumer):
        """Add consumer to topic."""
        if topic not in self.consumers:
            self.consumers[topic] = []
        self.consumers[topic].append(consumer)
    
    def get_topic_stats(self) -> Dict[str, Any]:
        """Get statistics for all topics."""
        stats = {}
        with self.lock:
            for topic, data in self.topics.items():
                total_messages = sum(len(partition) for partition in data['messages'])
                stats[topic] = {
                    'partitions': data['partitions'],
                    'total_messages': total_messages,
                    'consumers': len(self.consumers.get(topic, []))
                }
        return stats

class StreamProcessor:
    """Process streaming data with transformations."""
    
    def __init__(self, broker: StreamBroker):
        self.broker = broker
        self.processors = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def add_processor(self, name: str, input_topic: str, output_topic: str, 
                     transform_func: Callable[[Dict], Dict]):
        """Add a stream processor."""
        consumer = StreamConsumer(self.broker, f"processor_{name}")
        producer = StreamProducer(self.broker)
        
        def message_handler(message: StreamMessage):
            try:
                # Apply transformation
                transformed_data = transform_func(message.value)
                
                # Send to output topic
                producer.send(output_topic, message.key, transformed_data)
                
                self.logger.debug(f"Processed message in {name}")
            except Exception as e:
                self.logger.error(f"Error in processor {name}: {e}")
        
        consumer.set_message_handler(message_handler)
        consumer.subscribe([input_topic])
        
        self.processors[name] = {
            'consumer': consumer,
            'producer': producer,
            'input_topic': input_topic,
            'output_topic': output_topic
        }
        
        # Start processing in background thread
        thread = threading.Thread(target=consumer.start_consuming, daemon=True)
        thread.start()
        
        self.logger.info(f"Added processor: {name}")
    
    def stop_all_processors(self):
        """Stop all processors."""
        for name, processor in self.processors.items():
            processor['consumer'].stop_consuming()
            self.logger.info(f"Stopped processor: {name}")

class DataGenerator:
    """Generate sample streaming data."""
    
    def __init__(self, producer: StreamProducer):
        self.producer = producer
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def generate_user_events(self, topic: str = "user_events"):
        """Generate user event data."""
        self.running = True
        
        while self.running:
            try:
                event = {
                    'user_id': np.random.randint(1, 1000),
                    'event_type': np.random.choice(['click', 'view', 'purchase', 'signup']),
                    'page': np.random.choice(['home', 'product', 'cart', 'checkout']),
                    'timestamp': datetime.now().isoformat(),
                    'session_id': f"session_{np.random.randint(1, 100)}",
                    'value': np.random.uniform(0, 100)
                }
                
                self.producer.send(topic, f"user_{event['user_id']}", event)
                time.sleep(np.random.uniform(0.1, 2.0))  # Random delay
                
            except Exception as e:
                self.logger.error(f"Error generating user events: {e}")
    
    def generate_sensor_data(self, topic: str = "sensor_data"):
        """Generate IoT sensor data."""
        self.running = True
        
        while self.running:
            try:
                data = {
                    'sensor_id': f"sensor_{np.random.randint(1, 50)}",
                    'temperature': np.random.normal(25, 5),
                    'humidity': np.random.uniform(30, 80),
                    'pressure': np.random.normal(1013, 10),
                    'timestamp': datetime.now().isoformat(),
                    'location': np.random.choice(['warehouse_a', 'warehouse_b', 'office'])
                }
                
                self.producer.send(topic, data['sensor_id'], data)
                time.sleep(np.random.uniform(0.5, 3.0))
                
            except Exception as e:
                self.logger.error(f"Error generating sensor data: {e}")
    
    def stop_generation(self):
        """Stop data generation."""
        self.running = False

# Flask Web Dashboard
app = Flask(__name__)
broker = StreamBroker()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Data Streaming Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stat-value { font-size: 2em; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; margin-top: 5px; }
        .messages { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .message { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #007bff; }
        .controls { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .status.success { background: #d4edda; color: #155724; }
        .status.error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Real-Time Data Streaming Dashboard</h1>
            <p>Monitor and control your streaming data pipeline</p>
        </div>
        
        <div class="controls">
            <h3>Controls</h3>
            <button onclick="startGenerator('user_events')">Start User Events</button>
            <button onclick="startGenerator('sensor_data')">Start Sensor Data</button>
            <button onclick="stopGenerators()">Stop All Generators</button>
            <button onclick="refreshStats()">Refresh Stats</button>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be loaded here -->
        </div>
        
        <div class="messages">
            <h3>Recent Messages</h3>
            <div id="messagesList">
                <!-- Messages will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        let refreshInterval;
        
        function startGenerator(type) {
            fetch(`/start_generator/${type}`, {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    showStatus(data.message, data.status);
                    refreshStats();
                });
        }
        
        function stopGenerators() {
            fetch('/stop_generators', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    showStatus(data.message, data.status);
                    refreshStats();
                });
        }
        
        function refreshStats() {
            fetch('/stats')
                .then(response => response.json())
                .then(data => {
                    updateStatsGrid(data);
                });
        }
        
        function updateStatsGrid(stats) {
            const grid = document.getElementById('statsGrid');
            grid.innerHTML = '';
            
            for (const [topic, data] of Object.entries(stats)) {
                const card = document.createElement('div');
                card.className = 'stat-card';
                card.innerHTML = `
                    <div class="stat-value">${data.total_messages}</div>
                    <div class="stat-label">${topic} Messages</div>
                    <small>Partitions: ${data.partitions} | Consumers: ${data.consumers}</small>
                `;
                grid.appendChild(card);
            }
        }
        
        function showStatus(message, status) {
            const statusDiv = document.createElement('div');
            statusDiv.className = `status ${status}`;
            statusDiv.textContent = message;
            document.querySelector('.controls').appendChild(statusDiv);
            
            setTimeout(() => statusDiv.remove(), 3000);
        }
        
        // Auto-refresh stats every 5 seconds
        refreshInterval = setInterval(refreshStats, 5000);
        
        // Initial load
        refreshStats();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/stats')
def get_stats():
    """Get streaming statistics."""
    return jsonify(broker.get_topic_stats())

@app.route('/start_generator/<generator_type>', methods=['POST'])
def start_generator(generator_type):
    """Start data generator."""
    try:
        producer = StreamProducer(broker)
        generator = DataGenerator(producer)
        
        if generator_type == 'user_events':
            thread = threading.Thread(target=generator.generate_user_events, daemon=True)
            thread.start()
            return jsonify({'status': 'success', 'message': 'User events generator started'})
        elif generator_type == 'sensor_data':
            thread = threading.Thread(target=generator.generate_sensor_data, daemon=True)
            thread.start()
            return jsonify({'status': 'success', 'message': 'Sensor data generator started'})
        else:
            return jsonify({'status': 'error', 'message': 'Unknown generator type'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/stop_generators', methods=['POST'])
def stop_generators():
    """Stop all generators."""
    return jsonify({'status': 'success', 'message': 'All generators stopped'})

def main():
    """Main execution function."""
    print("Real-Time Data Streaming System")
    print("=" * 35)
    
    # Create topics
    broker.create_topic("user_events", partitions=3)
    broker.create_topic("sensor_data", partitions=2)
    broker.create_topic("processed_events", partitions=2)
    
    # Set up stream processor
    processor = StreamProcessor(broker)
    
    # Add event aggregation processor
    def aggregate_events(data):
        """Simple aggregation transformation."""
        return {
            **data,
            'processed_at': datetime.now().isoformat(),
            'event_score': data.get('value', 0) * 1.5
        }
    
    processor.add_processor(
        "event_aggregator",
        "user_events",
        "processed_events",
        aggregate_events
    )
    
    print("Starting web dashboard...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

