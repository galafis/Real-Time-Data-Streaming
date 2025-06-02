# Real-Time Data Streaming

[English](#english) | [Português](#português)

## English

### Overview
High-performance real-time data streaming system built with Python and Flask. Features live data ingestion, processing, and visualization with WebSocket support for real-time updates and scalable architecture for handling continuous data streams.

### Features
- **Real-Time Ingestion**: Live data streaming from multiple sources
- **WebSocket Support**: Real-time client updates and notifications
- **Data Processing**: Stream processing with filtering and aggregation
- **Scalable Architecture**: Designed for high-throughput data streams
- **Multiple Data Sources**: APIs, databases, file streams, IoT devices
- **Live Visualization**: Real-time charts and dashboards
- **Error Handling**: Robust error management and recovery
- **Monitoring**: Performance metrics and health checks

### Technologies Used
- **Python 3.8+**
- **Flask**: Web framework with WebSocket support
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **WebSockets**: Real-time communication
- **Threading**: Concurrent data processing

### Installation

1. Clone the repository:
```bash
git clone https://github.com/galafis/Real-Time-Data-Streaming.git
cd Real-Time-Data-Streaming
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the streaming system:
```bash
python streaming_system.py
```

4. Open your browser to `http://localhost:5000`

### Usage

#### Web Interface
1. **Start Stream**: Begin real-time data ingestion
2. **Monitor Data**: View live data flow and statistics
3. **Configure Sources**: Set up data source connections
4. **View Analytics**: Real-time charts and metrics
5. **Export Data**: Download processed data streams

#### API Endpoints

**Start Data Stream**
```bash
curl -X POST http://localhost:5000/api/stream/start \
  -H "Content-Type: application/json" \
  -d '{"source": "api", "interval": 1}'
```

**Get Stream Status**
```bash
curl -X GET http://localhost:5000/api/stream/status
```

**Stop Data Stream**
```bash
curl -X POST http://localhost:5000/api/stream/stop
```

#### Python API
```python
from streaming_system import DataStreamer

# Initialize streamer
streamer = DataStreamer()

# Configure data source
streamer.add_source('api', {
    'url': 'https://api.example.com/data',
    'interval': 5,
    'format': 'json'
})

# Start streaming
streamer.start_stream()

# Process data in real-time
for data_batch in streamer.get_stream():
    processed = streamer.process_data(data_batch)
    streamer.send_to_clients(processed)
```

### Data Sources

#### API Endpoints
- **REST APIs**: JSON/XML data ingestion
- **WebSocket APIs**: Real-time data feeds
- **Authentication**: API key and OAuth support

#### Database Streams
- **Change Data Capture**: Database change monitoring
- **Polling**: Periodic database queries
- **Triggers**: Event-driven data extraction

#### File Streams
- **CSV Files**: Continuous file monitoring
- **Log Files**: Real-time log processing
- **JSON Streams**: Structured data ingestion

#### IoT Devices
- **MQTT**: IoT device communication
- **Sensor Data**: Real-time sensor readings
- **Device Management**: Connection monitoring

### Stream Processing

#### Data Transformation
- **Filtering**: Remove unwanted data points
- **Aggregation**: Real-time calculations and summaries
- **Enrichment**: Add metadata and context
- **Validation**: Data quality checks

#### Real-Time Analytics
- **Moving Averages**: Sliding window calculations
- **Anomaly Detection**: Outlier identification
- **Pattern Recognition**: Trend analysis
- **Alerting**: Threshold-based notifications

### Performance Features

#### Scalability
- **Multi-Threading**: Concurrent data processing
- **Queue Management**: Buffer overflow protection
- **Load Balancing**: Distribute processing load
- **Memory Optimization**: Efficient data handling

#### Monitoring
- **Throughput Metrics**: Data processing rates
- **Latency Tracking**: End-to-end timing
- **Error Rates**: Failure monitoring
- **Resource Usage**: CPU and memory tracking

### Configuration
Configure streaming parameters in `config.json`:
```json
{
  "stream_config": {
    "buffer_size": 1000,
    "batch_size": 100,
    "processing_interval": 1,
    "max_connections": 50
  },
  "data_sources": [
    {
      "name": "api_source",
      "type": "api",
      "url": "https://api.example.com/stream",
      "interval": 5
    }
  ]
}
```

### WebSocket Events
- **data_update**: New data available
- **stream_status**: Stream health information
- **error_alert**: Error notifications
- **metrics_update**: Performance statistics

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Português

### Visão Geral
Sistema de streaming de dados em tempo real de alta performance construído com Python e Flask. Apresenta ingestão de dados ao vivo, processamento e visualização com suporte WebSocket para atualizações em tempo real e arquitetura escalável para lidar com fluxos contínuos de dados.

### Funcionalidades
- **Ingestão em Tempo Real**: Streaming de dados ao vivo de múltiplas fontes
- **Suporte WebSocket**: Atualizações e notificações em tempo real para clientes
- **Processamento de Dados**: Processamento de stream com filtragem e agregação
- **Arquitetura Escalável**: Projetada para fluxos de dados de alto throughput
- **Múltiplas Fontes de Dados**: APIs, bancos de dados, streams de arquivos, dispositivos IoT
- **Visualização ao Vivo**: Gráficos e dashboards em tempo real
- **Tratamento de Erros**: Gerenciamento robusto de erros e recuperação
- **Monitoramento**: Métricas de performance e verificações de saúde

### Tecnologias Utilizadas
- **Python 3.8+**
- **Flask**: Framework web com suporte WebSocket
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **WebSockets**: Comunicação em tempo real
- **Threading**: Processamento concorrente de dados

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/galafis/Real-Time-Data-Streaming.git
cd Real-Time-Data-Streaming
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o sistema de streaming:
```bash
python streaming_system.py
```

4. Abra seu navegador em `http://localhost:5000`

### Uso

#### Interface Web
1. **Iniciar Stream**: Começar ingestão de dados em tempo real
2. **Monitorar Dados**: Visualizar fluxo de dados ao vivo e estatísticas
3. **Configurar Fontes**: Configurar conexões de fontes de dados
4. **Ver Analytics**: Gráficos e métricas em tempo real
5. **Exportar Dados**: Download de streams de dados processados

#### Endpoints da API

**Iniciar Stream de Dados**
```bash
curl -X POST http://localhost:5000/api/stream/start \
  -H "Content-Type: application/json" \
  -d '{"source": "api", "interval": 1}'
```

**Obter Status do Stream**
```bash
curl -X GET http://localhost:5000/api/stream/status
```

**Parar Stream de Dados**
```bash
curl -X POST http://localhost:5000/api/stream/stop
```

#### API Python
```python
from streaming_system import DataStreamer

# Inicializar streamer
streamer = DataStreamer()

# Configurar fonte de dados
streamer.add_source('api', {
    'url': 'https://api.example.com/data',
    'interval': 5,
    'format': 'json'
})

# Iniciar streaming
streamer.start_stream()

# Processar dados em tempo real
for data_batch in streamer.get_stream():
    processed = streamer.process_data(data_batch)
    streamer.send_to_clients(processed)
```

### Fontes de Dados

#### Endpoints de API
- **APIs REST**: Ingestão de dados JSON/XML
- **APIs WebSocket**: Feeds de dados em tempo real
- **Autenticação**: Suporte para chave API e OAuth

#### Streams de Banco de Dados
- **Change Data Capture**: Monitoramento de mudanças no banco
- **Polling**: Consultas periódicas ao banco
- **Triggers**: Extração de dados orientada por eventos

#### Streams de Arquivos
- **Arquivos CSV**: Monitoramento contínuo de arquivos
- **Arquivos de Log**: Processamento de logs em tempo real
- **Streams JSON**: Ingestão de dados estruturados

#### Dispositivos IoT
- **MQTT**: Comunicação com dispositivos IoT
- **Dados de Sensores**: Leituras de sensores em tempo real
- **Gerenciamento de Dispositivos**: Monitoramento de conexões

### Processamento de Stream

#### Transformação de Dados
- **Filtragem**: Remover pontos de dados indesejados
- **Agregação**: Cálculos e resumos em tempo real
- **Enriquecimento**: Adicionar metadados e contexto
- **Validação**: Verificações de qualidade de dados

#### Analytics em Tempo Real
- **Médias Móveis**: Cálculos de janela deslizante
- **Detecção de Anomalias**: Identificação de outliers
- **Reconhecimento de Padrões**: Análise de tendências
- **Alertas**: Notificações baseadas em limites

### Funcionalidades de Performance

#### Escalabilidade
- **Multi-Threading**: Processamento concorrente de dados
- **Gerenciamento de Fila**: Proteção contra overflow de buffer
- **Balanceamento de Carga**: Distribuir carga de processamento
- **Otimização de Memória**: Manuseio eficiente de dados

#### Monitoramento
- **Métricas de Throughput**: Taxas de processamento de dados
- **Rastreamento de Latência**: Timing end-to-end
- **Taxas de Erro**: Monitoramento de falhas
- **Uso de Recursos**: Rastreamento de CPU e memória

### Configuração
Configure parâmetros de streaming em `config.json`:
```json
{
  "stream_config": {
    "buffer_size": 1000,
    "batch_size": 100,
    "processing_interval": 1,
    "max_connections": 50
  },
  "data_sources": [
    {
      "name": "api_source",
      "type": "api",
      "url": "https://api.example.com/stream",
      "interval": 5
    }
  ]
}
```

### Eventos WebSocket
- **data_update**: Novos dados disponíveis
- **stream_status**: Informações de saúde do stream
- **error_alert**: Notificações de erro
- **metrics_update**: Estatísticas de performance

### Contribuindo
1. Faça um fork do repositório
2. Crie uma branch de feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

### Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

