## **1. Inyección de dependencias**

La inyección de dependencias se observa en el patrón utilizado para instanciar el almacenamiento de imágenes. En el código la dependencia del sistema de almacenamiento de imágenes (`ImageStorage`) se inyecta en la vista a través de la fábrica de vistas `ImageViewFactory`. Esto significa que la dependencia (el almacenamiento de imágenes) no se crea directamente dentro de la vista, sino que se le pasa desde fuera, lo que hace que la vista no esté acoplada a una implementación específica de almacenamiento.

En el archivo `views.py` se usa la fábrica `ImageViewFactory`, que recibe una instancia de `ImageLocalStorage`:

```python
def ImageViewFactory(image_storage):
    class ImageView(View):
        # ...
```

Aquí, `image_storage` es la dependencia inyectada, y puede ser intercambiada fácilmente por otra implementación sin modificar el código de la vista.

### Ventajas:

- Facilita el testeo (se pueden pasar objetos simulados, o "mocks").
- Hace que las clases sean más reutilizables y desacopladas.
- Promueve el uso de principios SOLID (especialmente el de Inversión de Dependencias).

## **2. Inversión de dependencias**

La inversión de dependencias se aplica al definir la interfaz `ImageStorage` en el archivo `interfaces.py`. La vista no depende directamente de una implementación concreta de almacenamiento (por ejemplo, `ImageLocalStorage`), sino de la abstracción `ImageStorage`. De este modo, las clases de alto nivel (como la vista) dependen de abstracciones y no de implementaciones concretas.

Se define la abstracción `ImageStorage` como una interfaz:

```python
class ImageStorage(ABC):
    @abstractmethod
    def store(self, request: HttpRequest):
        pass
```

Luego, `ImageLocalStorage` implementa esta interfaz:

```python
class ImageLocalStorage(ImageStorage):
    def store(self, request: HttpRequest):
        # ...
```

La inversión de dependencias se da porque el código de la vista (`ImageViewFactory`) depende de la abstracción (`ImageStorage`), no de la implementación concreta (`ImageLocalStorage`).

## **3. Diferencias en la aplicación sin inversión de dependencias**

En este caso, la vista crea directamente una instancia de `ImageLocalStorage` en lugar de recibirla inyectada, lo que significa que la vista ahora está acoplada a una implementación específica.

Código sin inversión de dependencias:

```python
class ImageViewNoDI(View):
    def post(self, request):
        image_storage = ImageLocalStorage()  # Dependencia concreta
        image_url = image_storage.store(request)
```

En este enfoque, la vista depende de una clase de bajo nivel (`ImageLocalStorage`), lo que rompe el principio de DIP y hace más difícil cambiar el tipo de almacenamiento sin modificar el código de la vista.