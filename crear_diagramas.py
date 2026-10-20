from pathlib import Path
import xml.etree.ElementTree as E

BASE = Path(__file__).resolve().parent / 'docs'

class Diagram:
    def __init__(self, title, width=1600, height=1100):
        self.page = E.Element('diagram', name=title, id=title.replace(' ', '-'))
        model = E.SubElement(self.page, 'mxGraphModel', dx='1600', dy='1100', grid='1', gridSize='10', guides='1', tooltips='1', connect='1', arrows='1', fold='1', page='1', pageScale='1', pageWidth=str(width), pageHeight=str(height), math='0', shadow='0')
        self.root = E.SubElement(model, 'root')
        E.SubElement(self.root, 'mxCell', id='0')
        E.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.n = 1
        self.box(title, 30, 15, width-60, 45, 'text;html=0;fontSize=24;fontStyle=1;align=left;verticalAlign=middle;')

    def box(self, text, x, y, w, h, style=None):
        self.n += 1
        key = f'n{self.n}'
        c = E.SubElement(self.root, 'mxCell', id=key, value=text, style=style or 'rounded=1;whiteSpace=wrap;html=0;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;', vertex='1', parent='1')
        E.SubElement(c, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})
        return key

    def edge(self, source, target, text='', style='', points=None):
        self.n += 1
        c = E.SubElement(self.root, 'mxCell', id=f'e{self.n}', value=text, edge='1', parent='1', source=source, target=target, style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;fontSize=12;labelBackgroundColor=#ffffff;endArrow=open;endFill=0;'+style)
        g = E.SubElement(c, 'mxGeometry', relative='1', **{'as':'geometry'})
        if points:
            a = E.SubElement(g, 'Array', **{'as':'points'})
            for x,y in points: E.SubElement(a, 'mxPoint', x=str(x), y=str(y))

    def note(self, text, x, y, w=480, h=90):
        return self.box(text,x,y,w,h,'shape=note;whiteSpace=wrap;html=0;size=20;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=13;align=left;spacing=12;')

    def cls(self, name, attrs, ops, x, y, w=290):
        # Compartimientos UML independientes, agrupados por una clase contenedora.
        h1=40; h2=max(55, 22*len(attrs)+18); h3=max(45,22*len(ops)+18)
        parent=self.box('',x,y,w,h1+h2+h3,'rounded=0;html=0;fillColor=#ffffff;strokeColor=#6c8ebf;container=1;collapsible=0;')
        for label, yy, hh, bold, fill in [(name,0,h1,1,'#dae8fc'),('\n'.join(attrs),h1,h2,0,'#ffffff'),('\n'.join(ops),h1+h2,h3,0,'#ffffff')]:
            child=self.box(label,0,yy,w,hh,f'rounded=0;whiteSpace=wrap;html=0;fillColor={fill};strokeColor=#6c8ebf;fontSize=13;fontStyle={bold};align='+('center;' if bold else 'left;spacingLeft=10;'))
            self.root[-1].set('parent',parent)
        return parent

def save(folder, filename, pages):
    dest=BASE/folder/filename
    dest.parent.mkdir(parents=True,exist_ok=True)
    doc=E.Element('mxfile', host='app.diagrams.net', agent='MSGF', version='24.7.17', type='device', compressed='false')
    for p in pages: doc.append(p.page)
    E.indent(doc,space='  ')
    E.ElementTree(doc).write(dest,encoding='utf-8',xml_declaration=True)

def usecases(v2):
    d=Diagram('MSGF · Casos de uso · Iteración '+str(2 if v2 else 1),1600,1200)
    d.box('Sistema MSGF',300,90,990,970 if v2 else 670,'rounded=0;whiteSpace=wrap;html=0;fillColor=none;strokeColor=#666666;verticalAlign=top;fontSize=18;spacingTop=12;')
    actorstyle='shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=0;fontSize=14;'
    empleado=d.box('Empleado de la fundación',75,220,55,100,actorstyle)
    deudor=d.box('Deudor / pareja',1410,240,55,100,actorstyle)
    def uc(label,x,y):return d.box(label,x,y,260,65,'ellipse;whiteSpace=wrap;html=0;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;')
    fondos=uc('Calcular fondos disponibles',400,150)
    hip=uc('Gestionar hipotecas',400,270)
    inv=uc('Gestionar inversiones',400,390)
    rep=uc('Generar reporte semanal',850,150)
    pago=uc('Registrar pago de cuota',850,270)
    for node in [fondos,hip,inv,rep,pago]:d.edge(empleado,node,style='endArrow=none;')
    d.edge(deudor,pago,style='endArrow=none;')
    d.edge(rep,fondos,'«include»','dashed=1;')
    d.note('Gestionar hipotecas: crear, consultar, modificar y eliminar.\nGestionar inversiones: crear, consultar, modificar y retirar dinero.\nEl empleado registra las operaciones en MSGF.',360,505,770,95)
    d.note('Fondos para hipotecas = ingresos + cuotas pagadas + rendimientos de inversiones − gastos − subsidios a cuotas.\nEl reporte semanal consulta las hipotecas y las inversiones.',360,625,770,95)
    if v2:
        estudiante=d.box('Estudiante',1410,690,55,100,actorstyle)
        aporte=uc('Registrar aporte anual\npara becas-crédito',400,760)
        otorgar=uc('Otorgar beca-crédito\nsemestral',400,900)
        notas=uc('Registrar notas\ndel semestre',850,650)
        evaluar=uc('Evaluar notas y resolver\ncondonación o devolución',850,790)
        devolver=uc('Registrar devolución\nde matrícula',850,930)
        for node in [aporte,otorgar,notas,evaluar,devolver]:d.edge(empleado,node,style='endArrow=none;')
        for node in [notas,devolver]:d.edge(estudiante,node,style='endArrow=none;')
        d.edge(evaluar,notas,'«include»','dashed=1;')
        d.note('El estudiante presenta las notas cada semestre. El empleado las registra y aplica la política académica.\nCada beca-crédito financia la matrícula de un semestre.',340,1090,920,75)
    return d

def classes(v2):
    d=Diagram('MSGF · Modelo de clases · Iteración '+str(2 if v2 else 1),1900,1550 if v2 else 1100)
    activo=d.cls('«abstracta» Activo',['# numero: String','# valor: Decimal'],['+ consultarValor(): Decimal'],650,100)
    hip=d.cls('Hipoteca',['- pareja: String','- valorInicial: Decimal','- fecha: Date','- ingresoSemanal: Decimal','- saldo: Decimal'],['+ registrarCuota(valor: Decimal)','+ calcularSubsidio(): Decimal'],240,410,320)
    inv=d.cls('Inversión',['- fecha: Date','- tasaInteres: Decimal'],['+ registrarRendimiento(valor: Decimal)','+ retirarDinero(valor: Decimal)'],760,410,330)
    msg=d.cls('MSGF',['- ingresos: Decimal','- gastos: Decimal'],['+ calcularFondos(): Decimal','+ gestionarHipotecas()','+ gestionarInversiones()','+ generarReporteSemanal()'],1260,100,350)
    d.edge(hip,activo,style='endArrow=block;endFill=0;')
    d.edge(inv,activo,style='endArrow=block;endFill=0;')
    d.edge(msg,activo,'1 administra 0..*','endArrow=none;')
    cuota=d.cls('CuotaHipotecaria',['- fecha: Date','- valorPagado: Decimal','- subsidio: Decimal'],['+ registrarPago()'],230,760,330)
    d.edge(hip,cuota,'1 contiene 0..*','startArrow=diamond;startFill=1;endArrow=none;')
    d.note('Activo generaliza Hipoteca e Inversión.\nLos reportes son resultados calculados, no entidades persistentes.\nLos atributos y operaciones detallan el modelo inicial de las notas.',1180,490,560,120)
    if v2:
        aporte=d.cls('AporteAnualBecas',['- anio: Integer','- monto: Decimal','- saldoDisponible: Decimal'],['+ reservar(monto: Decimal)','+ consultarSaldo(): Decimal'],50,1120,310)
        beca=d.cls('BecaCrédito',['- id: String','- semestre: String','- costoMatricula: Decimal','- estado: EstadoBeca','- saldoPorDevolver: Decimal'],['+ otorgar()','+ registrarNotas()','+ resolverEvaluacion()','+ registrarDevolucion(valor: Decimal)'],610,1020,340)
        est=d.cls('Estudiante',['- documento: String','- nombre: String'],['+ consultarBecas()'],1130,900,300)
        notas=d.cls('RegistroNotas',['- semestre: String','- notas: Decimal [1..*]','- fechaPresentacion: Date'],['+ validar()'],1130,1190,300)
        pol=d.cls('PolíticaAcadémica',['- criterioCondonacion: String'],['+ cumple(notas: RegistroNotas): Boolean'],1510,1190,320)
        d.edge(msg,aporte,'1 administra 0..*','endArrow=none;',[(1740,80),(1740,730),(30,730),(30,1080)])
        d.edge(aporte,beca,'1 financia 0..*','endArrow=none;')
        d.edge(est,beca,'1 recibe 0..*','endArrow=none;')
        d.edge(beca,notas,'1 contiene 0..1','startArrow=diamond;startFill=1;endArrow=none;')
        d.edge(beca,pol,'usa para resolver','dashed=1;',[(990,1460),(1670,1460)])
        d.note('BecaCrédito representa un otorgamiento semestral. Un estudiante puede recibir varios.\nEl aporte anual financia los otorgamientos del año; no se mezcla automáticamente con los fondos hipotecarios.\nEl umbral de condonación y los plazos de devolución están pendientes de definición.',1180,650,600,150)
    return d

def states(v2):
    d=Diagram('MSGF · Máquina de estados del sistema · Iteración '+str(2 if v2 else 1),1600,1100)
    initial=d.box('',70,120,24,24,'ellipse;html=0;fillColor=#000000;strokeColor=#000000;')
    menu=d.box('Sistema en ejecución\nMenú principal',590,100,330,90)
    d.edge(initial,menu,'iniciar MSGF')
    specs=[('Cálculo de fondos','seleccionar calcular fondos',70,330),('Gestión de hipotecas','seleccionar hipotecas',450,330),('Gestión de inversiones','seleccionar inversiones',830,330),('Generación de reporte','seleccionar reporte',1210,330)]
    for title,event,x,y in specs:
        node=d.box(title,x,y,290,100)
        d.edge(menu,node,event)
        d.edge(node,menu,'finalizar / volver al menú',points=[(x+145,490),(550,490),(550,230)])
    final=d.box('',1330,130,30,30,'shape=doubleEllipse;html=0;fillColor=#000000;strokeColor=#000000;')
    d.edge(menu,final,'salir / cerrar MSGF')
    d.note('Operaciones internas:\nHipotecas: crear, consultar, modificar, eliminar y registrar cuotas.\nInversiones: crear, consultar, modificar y retirar dinero.\nEl cálculo aplica la fórmula de fondos; el reporte muestra el resumen semanal.',70,620,680,150)
    if v2:
        becas=d.box('Gestión de becas-crédito',920,650,340,100)
        d.edge(menu,becas,'seleccionar becas-crédito',points=[(1530,240),(1530,700)])
        d.edge(becas,menu,'finalizar / volver al menú',points=[(800,700),(800,550),(560,550),(560,190)])
        d.note('Operaciones internas de becas:\nRegistrar aporte anual; otorgar por semestre; registrar notas; resolver condonación o devolución; registrar devoluciones.\nEl ciclo de cada beca se detalla en la segunda página.',850,850,610,125)
    return d

def scholarship_states():
    d=Diagram('Beca-crédito · Ciclo de vida de un otorgamiento semestral',1600,1050)
    init=d.box('',60,140,25,25,'ellipse;fillColor=#000000;strokeColor=#000000;')
    granted=d.box('Otorgada\nMatrícula del semestre financiada',260,110,340,100)
    d.edge(init,granted,'otorgar [aporte anual con saldo suficiente]\n/ reservar costo de matrícula')
    pending=d.box('Pendiente de evaluación\nNotas del semestre registradas',260,360,340,100)
    d.edge(granted,pending,'presentar notas / registrar y validar notas')
    decision=d.box('',760,375,70,70,'rhombus;fillColor=#fff2cc;strokeColor=#d6b656;')
    d.edge(pending,decision,'evaluar según política académica')
    waived=d.box('Condonada\nSaldo por devolver = 0',1040,180,340,100)
    debt=d.box('Por devolver\nSaldo = costo de matrícula',1040,520,340,100)
    paid=d.box('Devuelta\nSaldo por devolver = 0',1040,790,340,90)
    d.edge(decision,waived,'[cumple criterio de condonación]\n/ condonar matrícula')
    d.edge(decision,debt,'[no cumple criterio de condonación]\n/ establecer obligación')
    d.edge(debt,debt,'registrar devolución parcial\n[0 < pago < saldo] / reducir saldo',points=[(1480,550),(1480,690),(1200,690)])
    d.edge(debt,paid,'registrar devolución [pago = saldo]\n/ liquidar obligación')
    end=d.box('',1490,800,30,30,'shape=doubleEllipse;fillColor=#000000;strokeColor=#000000;')
    d.edge(waived,end,'cerrar otorgamiento',points=[(1520,230),(1520,740)])
    d.edge(paid,end,'cerrar otorgamiento')
    d.note('Cada semestre corresponde a un nuevo otorgamiento.\nLa evaluación decide sobre el costo completo de la matrícula del semestre.\nLa política académica no tiene un promedio mínimo definido en el enunciado.\nSe admite registrar devoluciones parciales como supuesto operativo; no se presuponen intereses ni fechas de vencimiento.',70,680,690,180)
    return d

def boundary(v2):
    d=Diagram('MSGF · Clases límite y control · Iteración '+str(2 if v2 else 1),1600,1250 if v2 else 1000)
    actor=d.box('Empleado',60,140,55,100,'shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=0;fontSize=14;')
    ui=d.box('«boundary»\nInterfazUsuarioMSGF\n\nmostrarMenú()\ncapturarDatos()\nmostrarResultados()',240,130,330,160)
    ctrl=d.box('«control»\nGestorMSGF\n\ncoordinarOperaciones()\ncalcularFondos()\ngenerarReporteSemanal()',760,130,350,160,'rounded=1;whiteSpace=wrap;html=0;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=14;')
    d.edge(actor,ui,style='endArrow=none;')
    d.edge(ui,ctrl,'solicita operación')
    hip=d.box('«entity»\nHipoteca',650,490,260,80)
    inv=d.box('«entity»\nInversión',1030,490,260,80)
    d.edge(ctrl,hip,'consulta / actualiza')
    d.edge(ctrl,inv,'consulta / actualiza')
    d.note('Límite: interacción con el empleado, entrada y salida de datos.\nControl: coordina casos de uso y cálculos.\nEntidad: información persistente del dominio.\nLas flechas muestran solicitudes; no representan herencia.',70,670,600,140)
    if v2:
        ui2=d.box('«boundary»\nInterfazBecasCrédito\n\ncapturarAporte()\ncapturarOtorgamiento()\ncapturarNotas()\ncapturarDevolucion()',240,870,330,210)
        ctrl2=d.box('«control»\nGestorBecasCrédito\n\nregistrarAporteAnual()\notorgarBecaSemestral()\nevaluarNotas()\nregistrarDevolucion()',760,850,350,210,'rounded=1;whiteSpace=wrap;html=0;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=14;')
        ent=d.box('«entity»\nAporteAnualBecas\nEstudiante\nBecaCrédito\nRegistroNotas\nPolíticaAcadémica',1250,850,280,190)
        d.edge(actor,ui2,style='endArrow=none;',points=[(150,300),(150,970)])
        d.edge(ui,ui2,'abre módulo',points=[(600,350),(600,820),(400,820)])
        d.edge(ui2,ctrl2,'solicita operación')
        d.edge(ctrl2,ent,'consulta / actualiza')
        d.note('El estudiante aporta notas y devuelve la matrícula cuando corresponde.\nSe supone que el empleado registra estos datos; el enunciado no exige un portal estudiantil.',760,1100,720,85)
    return d

for v2 in (False,True):
    folder='iteración2' if v2 else 'iteración1'
    save(folder,'01-casos-de-uso.drawio',[usecases(v2)])
    save(folder,'02-clases.drawio',[classes(v2)])
    save(folder,'03-maquina-de-estados.drawio',[states(v2)]+([scholarship_states()] if v2 else []))
    save(folder,'04-limite-y-control.drawio',[boundary(v2)])

(BASE/'README.md').write_text('''# Diagramas de MSGF

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
''',encoding='utf-8')

# Verificación estructural de todos los documentos XML y de sus referencias.
for path in BASE.rglob('*.drawio'):
    root=E.parse(path).getroot()
    for page in root.findall('diagram'):
        cells=page.findall('./mxGraphModel/root/mxCell')
        ids={c.get('id') for c in cells}
        assert len(ids)==len(cells),path
        for c in cells:
            for key in ('source','target','parent'):
                if c.get(key): assert c.get(key) in ids,(path,c.get(key))
    print(f'OK: {path.relative_to(BASE)} ({len(root.findall("diagram"))} página(s))')

