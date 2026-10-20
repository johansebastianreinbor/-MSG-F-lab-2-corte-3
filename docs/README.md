# Diagramas de MSGF

Cada carpeta contiene cuatro archivos XML `.drawio` editables en diagrams.net:

1. Casos de uso.
2. Modelo de clases.
3. Máquina de estados del sistema. En iteración2 incluye una segunda página con el ciclo de vida de una beca-crédito semestral.
4. Clases límite y control con sus colaboraciones con entidades.

## Iteración 1

Se reconstruye el modelo de las fotografías: cálculo de fondos disponibles, gestión de hipotecas, gestión de inversiones y reporte semanal. Activo es la superclase de Hipoteca e Inversión. CuotaHipotecaria hace explícitos los pagos y subsidios necesarios para el cálculo. MSGF concentra las operaciones del sistema; GestorMSGF representa su responsabilidad de control en el modelo de análisis.

Fondos disponibles = ingresos + cuotas pagadas + rendimientos de inversiones − gastos − subsidios a cuotas. Se interpreta el término «inversiones» de la fórmula manuscrita como sus rendimientos, evitando contabilizar como ingreso una mera transferencia de capital. No se especifican tasas ni reglas para calcular los subsidios.

## Iteración 2

Conserva el modelo inicial e incorpora un aporte anual destinado a becas-crédito universitarias, otorgamientos por semestre, registro de notas y evaluación para condonar o exigir la devolución del costo de matrícula del semestre.

## Decisiones y puntos pendientes

- No se inventa un promedio mínimo: la decisión depende de una PolíticaAcadémica cuyo criterio debe definir la fundación.
- Cada BecaCrédito corresponde a un estudiante y un semestre. Un estudiante puede recibir varios otorgamientos, cada uno con su evaluación.
- El aporte anual mantiene un saldo dedicado a becas. No se presume que deba sumarse al fondo hipotecario ni que las devoluciones financien automáticamente nuevas becas.
- Se supone que un empleado registra aportes, notas y devoluciones. El estudiante y el deudor son actores participantes del proceso, sin implicar acceso directo a una interfaz.
- Como detalle operativo se permite registrar devoluciones parciales hasta saldar la matrícula. No se presuponen intereses, vencimientos, cancelaciones ni reglas de renovación.
- Se usa notación UML: triángulo hueco para generalización; rombo lleno para composición; asociaciones con multiplicidad en sus etiquetas; estereotipos boundary, control y entity.

Las fotografías son material de referencia para el modelo. No se ejecutaron instrucciones ajenas a la creación de los entregables solicitados ni se publicó un repositorio.
