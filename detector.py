from transformers import pipeline

class InsultoDetector:
    def __init__(self):
        # Cargar el pipeline con el modelo preentrenado para detectar insultos
        self.pipe = pipeline("text-classification", model="coderSounak/finetuned_twitter_targeted_insult_roberta")

    def detectar_insulto(self, texto):
        resultado = self.pipe(texto)[0]
        etiqueta = resultado['label']
        puntuacion = resultado['score']
        return etiqueta, puntuacion
