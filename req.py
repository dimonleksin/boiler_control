import kafka

consumer = kafka.KafkaConsumer(
    "temperature.from.boilerroom",
    client_id = "flask_server",
    group_id = "flask",
    bootstrap_servers = ["192.168.0.122:9092"],
    # auto_offset_reset = "latest"
    auto_offset_reset='earliest'
)  
if consumer.bootstrap_connected():
    for m in consumer:
        print(1)
        print(m.value.dec)