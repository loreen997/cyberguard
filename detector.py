from transformers import pipeline


class InsultoDetector:
    def __init__(self):
        # Cargar el pipeline con el modelo preentrenado para detectar insultos
        self.pipe = pipeline("text-classification", model="coderSounak/finetuned_twitter_targeted_insult_roberta")

    def detectar_insulto(self, texto):
        resultado = self.pipe(texto)[0]  # El pipeline devuelve una lista, tomamos el primer resultado
        etiqueta = resultado['label']  # Obtener la etiqueta de clasificación
        puntuacion = resultado['score']  # Obtener la puntuación de confianza
        return etiqueta, puntuacion


