import google.generativeai as genai


operation = genai.create_tuned_model(
	source_model="gemini-1.0-pro-001",
	training_data=[{"text_input": "1", "output": "3"}],
	id="hd2024-recycle",
	epoch_count=100,
	batch_size=4,
	learning_rate=0.001	
)

tuned_model = operation.result()
