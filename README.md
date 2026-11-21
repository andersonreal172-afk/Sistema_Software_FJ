# Sistema Software FJ

Sistema integral en Python para gestionar clientes, servicios y reservas,
desarrollado con programación orientada a objetos y manejo robusto de
excepciones.

## Ejecutar

```powershell
python main.py
```

La opción 4 del menú ejecuta simulaciones válidas e inválidas. Los eventos y
errores se registran en `logs/sistema.log`.

## Funcionalidades

- Clase abstracta `Servicio` e implementaciones para salas, equipos y asesorías.
- Encapsulación mediante atributos privados y propiedades.
- Gestión en memoria de clientes, servicios y reservas.
- Excepciones personalizadas y encadenamiento de errores.
- Bloques `try/except`, `try/except/else`, `try/except/finally`.
- Registro de operaciones con el módulo `logging`.
- Menú interactivo por consola.

## Archivos principales

- `Servicio.py`: abstracción y excepciones de servicios.
- `ServiciosEspecializados.py`: implementaciones concretas.
- `Cliente.py`: modelo de cliente.
- `Reserva.py`: modelo de reserva.
- `SistemaGestion.py`: gestión y registro de eventos.
- `main.py`: menú y simulaciones.

## Participación de colaboradores

- John Anderson Real Niño
- Freddy Yesid Rivera Moyano
- Hugo Alejandro Hernandez Peña
- Diego Octavio Peñuela Colmenares
