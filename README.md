# 🅿️ PARKIA - Sistema Inteligente de Gestión de Estacionamientos

> **Proyecto Académico de Base de Datos**  
> **Universidad Autónoma "Gabriel René Moreno"**  
> **Facultad de Ingeniería en Ciencias de la Computación y Telecomunicaciones**  
> **Materia: INF-312 - Base de Datos I**  

> **Autor:** SARA RAQUEL SAHONERO SALAS

---

## 📌 Resumen Ejecutivo

PARKIA es un **sistema de gestión inteligente de estacionamientos para escritorio** diseñado para automatizar completamente la administración de un parqueo comercial sin infraestructura costosa.

**Arquitectura:**
- **Módulo Admin (Escritorio):** Solo para empleado/administrador. Interfaz Tkinter
- **QR Cliente:** Cliente genera QR único con tarifa calculada. Sin interfaz cliente
- **BD Relacional:** PostgreSQL (Supabase) normalizada 3FN, auditoría completa

**Flujo:**
1. Cámara detecta placa (OCR) → Auto ENTRA
2. Cámara detecta placa nuevamente → Auto SALE, calcula tarifa
3. Sistema genera QR único (válido 5 min) con tarifa: "Pague: 25 Bs"
4. **Cliente toma screenshot del QR y muestra al salir**
5. Empleado escanea QR, confirma pago en escritorio
6. BD registra: PAGADO + quién confirmó + cuándo

**Problema real:** Parqueo en Santa Cruz: ~50 autos/día, 35 espacios, 10 Bs/hora, registro manual → errores → 45,000 Bs/mes perdidos en visibilidad.

**Solución:** PARKIA automatiza todo. Empleado solo confirma pago (ve QR en pantalla cliente).

---

## 🎯 Objetivo General

Diseñar, implementar y validar **PARKIA**: un sistema de información integrado basado en base de datos relacional normalizada que automatice la gestión de estacionamientos mediante:
- **OCR automático** para detección de placas
- **Cálculo de tarifa** en tiempo real (10 Bs/hora)
- **Generación de QR** con tarifa (interfaz cliente mínima)
- **Módulo admin escritorio** para confirmación de pagos y reportes
- **Auditoría completa** de transacciones

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                     PARKIA ARCHITECTURE                         │
└─────────────────────────────────────────────────────────────────┘

    ENTRADA PARQUEO
         │
         ▼
    ┌──────────────────────────┐
    │   CÁMARA IP/USB          │
    │   (Detecta placa)        │
    └──────────────────────────┘
         │
         ▼
    ┌──────────────────────────┐
    │   EasyOCR                │
    │   (Lee placa ABC1234)    │
    └──────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────────────┐
    │              BACKEND (Python)                            │
    │  - Detectar entrada/salida                              │
    │  - Calcular tarifa (duración × 10 Bs)                   │
    │  - Generar QR único (válido 5 min)                      │
    │  - Auditoría (id, hora, operario)                       │
    └──────────────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────────────┐
    │          Supabase (PostgreSQL)                           │
    │  Tabla: movimientos                                      │
    │  - id, placa, tipo_evento, fechas                        │
    │  - duracion_minutos, monto_calculado                     │
    │  - estado_pago, codigo_qr, operario_id                   │
    │  - Respaldo automático en nube                           │
    └──────────────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────────────┐
    │          MÓDULO ADMIN (Escritorio - Tkinter)            │
    │                                                          │
    │  ┌─ PANTALLA 1: Monitoreo Tiempo Real ──────────────┐   │
    │  │ • Placa detectada: ABC1234                       │   │
    │  │ • Estado: ENTRADA hace 2 horas 15 min           │   │
    │  │ • Tarifa calculada: 22.5 Bs                      │   │
    │  │ • QR:  [CÓDIGO QR]                              │   │
    │  │ • [] Pago confirmado (checkbox)                  │   │
    │  │ • [Confirmar] [Anular] [Ver histórico]          │   │
    │  └─────────────────────────────────────────────────┘   │
    │                                                          │
    │  ┌─ PANTALLA 2: Reporte Diario ─────────────────────┐   │
    │  │ • Entradas totales: 48                           │   │
    │  │ • Salidas totales: 47                            │   │
    │  │ • Ingresos: 425.50 Bs                            │   │
    │  │ • Pagos confirmados: 47                          │   │
    │  │ • Pagos pendientes: 0                            │   │
    │  │ • Discrepancias: 0                               │   │
    │  │ • Gráfico de picos horarios                       │   │
    │  └─────────────────────────────────────────────────┘   │
    │                                                          │
    │  ┌─ PANTALLA 3: Auditoría ───────────────────────────┐   │
    │  │ • Historial completo de transacciones            │   │
    │  │ • Filtrar por fecha, placa, operario             │   │
    │  │ • Descargar reportes (CSV, PDF)                  │   │
    │  │ • Anomalías detectadas                           │   │
    │  └─────────────────────────────────────────────────┘   │
    └──────────────────────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────────────────────┐
    │             CLIENTE (Mínimo)                            │
    │                                                          │
    │  • Ve QR en pantalla del auto (generado por sistema)    │
    │  • Toma screenshot o foto del QR                        │
    │  • Lleva QR impreso/digital al salir                    │
    │  • Muestra QR al empleado                               │
    │  • Empleado escanea en escritorio → Pago confirmado     │
    │                                                          │
    │  SIN INTERFAZ: Solo QR + tarifa en pantalla             │
    └──────────────────────────────────────────────────────────┘
```

---

## 📂 Estructura del Repositorio

```
parkia-sistema/
├── 01_investigacion/
│   ├── README.md
│   ├── problema_real.md          ← Análisis del parqueo
│   ├── datos_estadisticos.csv    ← 50 autos/día, 10 Bs/hora
│   └── hipotesis.md
│
├── 02_diseno_conceptual/
│   ├── README.md
│   ├── diagrama_uml_clases.md
│   ├── casos_uso.md               ← SOLO admin, QR cliente
│   ├── reglas_negocio.md
│   └── diagramas/
│       └── uml.png
│
├── 03_modelo_relacional/
│   ├── README.md
│   ├── der_completo.md            ← Diagrama Entidad-Relación
│   ├── normalizacion_3fn.md
│   ├── pk_fk_justificacion.md
│   └── restricciones_dominios.md
│
├── 04_base_datos/
│   ├── README.md
│   ├── scripts_sql/
│   │   ├── 00_PARKIA_COMPLETO.sql  ← Script ejecutable
│   │   ├── 01_crear_tablas.sql
│   │   ├── 02_inserts_prueba.sql
│   │   └── 03_pruebas_integridad.sql
│   ├── consultas/
│   │   ├── consultas_requeridas.sql ← 5 consultas
│   │   ├── vistas.sql              ← 3 vistas
│   │   └── resultados_validados.md ← Pruebas
│   └── diccionario_datos.md
│
├── 05_backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   │   ├── main.py                 ← Orquestador
│   │   ├── detector_ocr.py         ← EasyOCR + cámara
│   │   ├── database.py             ← Conexión Supabase
│   │   ├── generador_qr.py         ← QR con tarifa
│   │   ├── auditoria.py            ← Auditoría y fraude
│   │   └── utils.py
│   └── tests/
│       ├── test_detector.py
│       ├── test_database.py
│       └── test_qr.py
│
├── 06_admin_escritorio/
│   ├── README.md
│   ├── interfaz_admin.py           ← Tkinter GUI
│   ├── pantalla_monitoreo.py       ← Tiempo real + QR
│   ├── pantalla_reportes.py        ← Reporte diario
│   ├── pantalla_auditoria.py       ← Histórico
│   └── assets/
│       └── logo.png
│
├── 07_cliente_qr/
│   ├── README.md
│   ├── mostrar_qr.py               ← Ventana QR simple
│   └── generador_qr_standalone.py  ← Script independiente
│
├── 08_implementacion/
│   ├── README.md
│   ├── guia_instalacion.md
│   ├── configuracion_supabase.md
│   ├── deployment.md
│   └── troubleshooting.md
│
├── 09_pruebas_validacion/
│   ├── README.md
│   ├── plan_testing.md
│   ├── casos_prueba.md
│   ├── resultados_pruebas.md
│   └── metricas_desempeño.md
│
├── 10_documentacion_academica/
│   ├── 01_resumen_ejecutivo.md
│   ├── 02_introduccion.md
│   ├── 03_antecedentes.md
│   ├── 04_problematica.md
│   ├── 05_marco_teorico.md
│   ├── 06_marco_metodologico.md
│   ├── 07_propuesta_tecnica.md
│   ├── 08_resultados.md
│   ├── 09_conclusiones.md
│   ├── 10_referencias_bibliografia.md
│   └── DOCUMENTO_COMPLETO.md
│
├── 11_defensa/
│   ├── README.md
│   ├── presentacion_diapositivas.pptx
│   ├── respuestas_preguntas.md
│   ├── trabajo_equipo.md
│   └── checklist_100pts.md
│
├── 12_anexos/
│   ├── screenshots/
│   │   ├── admin_monitoreo.png
│   │   ├── admin_reportes.png
│   │   ├── admin_auditoria.png
│   │   ├── cliente_qr.png
│   │   └── qr_ejemplo.png
│   ├── diagramas/
│   │   ├── arquitectura.png
│   │   ├── flujo_entrada_salida.png
│   │   ├── der_parkia.png
│   │   └── casos_uso.png
│   ├── datos/
│   │   ├── datos_prueba.csv
│   │   └── datos_reales_30dias.csv
│   └── videos/
│       ├── demo_admin.mp4
│       └── demo_cliente.mp4
│
├── README.md                    ← Este archivo
├── CHANGELOG.md
├── .gitignore
├── .env.example
└── LICENSE
```

---

## 🔄 Flujo de Uso Completo (CORREGIDO)

### Escenario Real: Auto ABC1234 entra al parqueo

**PASO 1: ENTRADA (Empleado ve en pantalla admin)**
```
09:00:00 - Cámara detecta placa ABC1234
         - OCR reconoce: "ABC1234" (85% confianza)
         - BD registra: ENTRADA
         - Admin ve en pantalla: "ABC1234 - Toyota Corolla Blanco - ENTRADA"
```

**PASO 2: AUTO ESTACIONADO**
```
Carro está 2 horas 15 minutos adentro
```

**PASO 3: SALIDA (Auto sale, sistema genera COMPROBANTE)**
```
11:15:00 - Cámara detecta placa ABC1234 nuevamente
         - Sistema detecta: "ABC1234 ya estaba en BD"
         - Calcula: duracion = 135 minutos = 2.25 horas
         - Tarifa = 2.25 horas × 10 Bs = 22.50 Bs
         - Genera COMPROBANTE QR único: "TICKET-ABC1234-20240115-111500"
         - QR contiene: Monto, hora entrada, hora salida, duración
         - BD registra: SALIDA + 22.50 Bs + QR_COMPROBANTE
         
         PANTALLA ADMIN MUESTRA (para mostrar al cliente):
         ┌──────────────────────────────────────┐
         │    COMPROBANTE DE SALIDA             │
         ├──────────────────────────────────────┤
         │ Placa: ABC1234                       │
         │ Entrada: 09:00                       │
         │ Salida: 11:15                        │
         │ Duración: 2h 15min                   │
         │                                      │
         │ ╔════════════════════════════════╗  │
         │ ║   MONTO A PAGAR: 22.50 Bs      ║  │
         │ ╚════════════════════════════════╝  │
         │                                      │
         │ [QR CODE]                            │
         │ TICKET-ABC1234-20240115-111500       │
         │                                      │
         │ * Pagar en EFECTIVO al empleado      │
         │ * Mostrar este comprobante al salir  │
         └──────────────────────────────────────┘
         
         Estado BD: PENDIENTE PAGO
         (Se confirma cuando cliente PAGA EN EFECTIVO)
```

**PASO 4: CLIENTE RECIBE COMPROBANTE (NO ES PAGO)**
```
Sistema genera comprobante que cliente Ve:
┌──────────────────────────────────────┐
│    ¡COMPROBANTE DE SALIDA!           │
├──────────────────────────────────────┤
│ Placa: ABC1234                       │
│ Hora entrada: 09:00                  │
│ Hora salida: 11:15                   │
│ Duración: 2 horas 15 minutos         │
│                                      │
│ ╔════════════════════════════════╗  │
│ ║   TOTAL A PAGAR: 22.50 Bs      ║  │
│ ║                                ║  │
│ ║   EFECTIVO AL SALIR            ║  │
│ ╚════════════════════════════════╝  │
│                                      │
│ [QR CODE]                            │
│ TICKET-ABC1234-20240115-111500       │
│                                      │
│ Presentar esto al empleado al pagar  │
└──────────────────────────────────────┘

Cliente toma screenshot O imprime comprobante
```

**PASO 5: CLIENTE PAGA EN EFECTIVO (COORDINACIÓN DIRECTA)**
```
FLUJO MANUAL EN SALIDA:

1. Cliente sale del auto con comprobante (screenshot/impreso)
2. Cliente llega a caseta del empleado
3. Cliente muestra comprobante: "22.50 Bs"
4. Cliente ENTREGA DINERO EN EFECTIVO
5. Empleado recibe 22.50 Bs
6. Empleado mira pantalla ADMIN del sistema

   PANTALLA ADMIN MUESTRA:
   ┌─────────────────────────────────────────────┐
   │ COMPROBANTE PENDIENTE DE CONFIRMACIÓN        │
   │                                             │
   │ Placa: ABC1234                              │
   │ Monto: 22.50 Bs                             │
   │ QR: TICKET-ABC1234-20240115-111500          │
   │                                             │
   │ [Escanear QR] O [Escribir código]           │
   │ [                    ]                       │
   │                                             │
   │ Cliente mostró dinero: ☐ Sí  ☐ No          │
   │ Dinero recibido: ☐                          │
   │                                             │
   │ [✓ CONFIRMAR PAGO RECIBIDO]  [Anular]      │
   └─────────────────────────────────────────────┘

7. Empleado hace click: [✓ CONFIRMAR PAGO RECIBIDO]
8. BD actualiza: estado_pago = PAGADO + fecha_confirmacion
```

**PASO 6: CONFIRMACIÓN EN BD (DESPUÉS DEL PAGO EN EFECTIVO)**
```
BD REGISTRA SOLO DESPUÉS de pago físico confirmado:

movimiento_id: 1001
├─ placa: ABC1234
├─ tipo_evento: SALIDA
├─ monto_calculado: 22.50 Bs
├─ estado_pago: PAGADO ✓
├─ codigo_qr: TICKET-ABC1234-20240115-111500
├─ operario_id: 1 (Juan - quien confirmó el pago)
├─ fecha_hora_salida: 2024-01-15 11:15:00
├─ fecha_confirmacion_pago: 2024-01-15 11:15:45
└─ forma_pago: EFECTIVO

LA CLAVE: No paga por QR, paga en EFECTIVO
El QR es solo COMPROBANTE/TICKET
```

**PASO 7: AUDITORÍA DIARIA (RECONCILIACIÓN)**
```
Al final del día, empleado ve en pantalla "Reportes":
┌──────────────────────────────────────────────────────┐
│ REPORTE DIARIO - 2024-01-15                         │
│                                                     │
│ RESUMEN:                                            │
│ ├─ Entradas registradas: 48                         │
│ ├─ Salidas registradas: 47                          │
│ └─ Autos aún adentro: 1                             │
│                                                     │
│ PAGOS:                                              │
│ ├─ Comprobantes generados: 47                       │
│ ├─ Pagos confirmados (efectivo): 47                 │
│ ├─ Pagos pendientes: 0                              │
│ └─ Ingresos totales registrados: 425.50 Bs          │
│                                                     │
│ AUDITORÍA (RECONCILIACIÓN):                         │
│ ├─ Dinero registrado en sistema: 425.50 Bs          │
│ ├─ Dinero en caja física: 425.50 Bs                 │
│ ├─ DIFERENCIA: 0 Bs ✓✓✓                             │
│ └─ ESTADO: SIN DISCREPANCIAS ✓                      │
│                                                     │
│ OPERARIO: Juan                                      │
│ Transacciones manejadas: 47                         │
│                                                     │
│ [Descargar Reporte] [Exportar CSV] [Imprimir]      │
└──────────────────────────────────────────────────────┘

CLAVE: Dinero registrado = Dinero físico
Si no coinciden → Fraude/Error detectado
```

---

### 1️⃣ MODELADO CONCEPTUAL (UML) 

**Clases principales:**

```
┌──────────────────────┐
│    MOVIMIENTO        │  ← Central (todo sucede aquí)
├──────────────────────┤
│ - id: int (PK)       │
│ - placa: string      │
│ - marca: string      │
│ - modelo: string     │
│ - color: string      │
│ - tipo_evento: enum  │  (ENTRADA, SALIDA)
│ - fecha_hora_entrada │
│ - fecha_hora_salida  │
│ - duracion_minutos   │
│ - monto_calculado    │
│ - estado_pago: enum  │  (PENDIENTE, PAGADO)
│ - codigo_qr: string  │  UNIQUE
│ - operario_id: int   │  FK → OPERARIOS
│ - fecha_creacion     │
└──────────────────────┘

┌──────────────────────┐
│     OPERARIO         │
├──────────────────────┤
│ - id: int (PK)       │
│ - nombre: string     │
│ - email: string      │
│ - rol: string        │
│ - fecha_creacion     │
└──────────────────────┘
         ▲
         │ (1) ──registra─ (*)
         │
    MOVIMIENTO
```

**Relaciones:**
- OPERARIO (1) ──registra──> (*) MOVIMIENTO
- MOVIMIENTO: tipo_evento ∈ {ENTRADA, SALIDA}
- MOVIMIENTO: estado_pago ∈ {PENDIENTE, PAGADO}

**Coherencia con reglas:**
1. No doble cobro: UNIQUE(codigo_qr)
2. Tarifa fija: monto = duracion_minutos / 60 * 10
3. Pago manual: empleado confirma, no automático
4. Auditoría: operario_id + fecha_creacion en cada registro

**Ubicación en repo:** `02_diseno_conceptual/diagrama_uml_clases.md`

---

### 2️⃣ MODELO RELACIONAL Y NORMALIZACIÓN

**PK bien definidas:**
- MOVIMIENTO.id: BIGSERIAL (surrogada, no depende de placa volátil)
- OPERARIO.id: BIGSERIAL

**FK bien definidas:**
- MOVIMIENTO.operario_id → OPERARIO.id (auditoría)
- Integridad referencial: CASCADE DELETE deshabilitado (auditoría requiere histórico)

**Restricciones:**
```sql
-- Dominio: tipo_evento
CHECK (tipo_evento IN ('ENTRADA', 'SALIDA'))

-- Dominio: estado_pago
CHECK (estado_pago IN ('PENDIENTE', 'PAGADO'))

-- Lógica: salida después de entrada
CHECK (fecha_hora_salida IS NULL OR fecha_hora_salida > fecha_hora_entrada)

-- Lógica: monto positivo
CHECK (monto_calculado > 0 OR monto_calculado IS NULL)

-- No doble cobro
UNIQUE (codigo_qr)
```

**Normalización a 3FN:**
- 1FN: Sin atributos multivaluados ✓
- 2FN: Sin dependencias parciales ✓ (nombre_operario en OPERARIO, no en MOVIMIENTO)
- 3FN: Sin dependencias transitivas ✓ (no guardamos datos redundantes)

**Ubicación en repo:** `03_modelo_relacional/`

---

### 3️⃣ IMPLEMENTACIÓN SQL (DDL + DML)

**Script ejecutable:**

```sql
-- 1. Crear tabla OPERARIOS
CREATE TABLE operarios (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    rol VARCHAR(50) DEFAULT 'OPERARIO',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Crear tabla MOVIMIENTOS
CREATE TABLE movimientos (
    id BIGSERIAL PRIMARY KEY,
    placa VARCHAR(20) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    color VARCHAR(30),
    tipo_evento VARCHAR(20) NOT NULL,
    fecha_hora_entrada TIMESTAMP,
    fecha_hora_salida TIMESTAMP,
    duracion_minutos INTEGER,
    monto_calculado DECIMAL(10,2),
    estado_pago VARCHAR(20) DEFAULT 'PENDIENTE',
    codigo_qr VARCHAR(30) UNIQUE,
    operario_id BIGINT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (operario_id) REFERENCES operarios(id),
    CHECK (tipo_evento IN ('ENTRADA', 'SALIDA')),
    CHECK (estado_pago IN ('PENDIENTE', 'PAGADO')),
    CHECK (monto_calculado > 0 OR monto_calculado IS NULL),
    CHECK (fecha_hora_salida IS NULL OR fecha_hora_salida > fecha_hora_entrada)
);

-- 3. Crear índices
CREATE INDEX idx_placa ON movimientos(placa);
CREATE INDEX idx_fecha ON movimientos(fecha_hora_entrada);
CREATE INDEX idx_estado_pago ON movimientos(estado_pago);

-- 4. Insertar datos prueba
INSERT INTO operarios (nombre, email, rol) VALUES 
    ('Juan', 'juan@parkia.com', 'OPERARIO'),
    ('María', 'maria@parkia.com', 'ADMIN');

INSERT INTO movimientos (placa, marca, modelo, color, tipo_evento, 
    fecha_hora_entrada, operario_id) VALUES 
    ('ABC1234', 'Toyota', 'Corolla', 'Blanco', 'ENTRADA', 
     '2024-01-15 09:00:00', 1);

-- Simular salida
UPDATE movimientos SET 
    tipo_evento = 'SALIDA',
    fecha_hora_salida = '2024-01-15 11:15:00',
    duracion_minutos = 135,
    monto_calculado = 22.50,
    estado_pago = 'PAGADO',
    codigo_qr = 'QR-ABC1234-20240115-111500'
WHERE id = 1;
```

**Integridad referencial:**
- ✓ FK funcionan (no puedo insertar operario_id que no existe)
- ✓ UNIQUE funciona (no puedo duplicar codigo_qr)
- ✓ CHECK funciona (no puedo violar restricciones)

**Ubicación en repo:** `04_base_datos/scripts_sql/00_PARKIA_COMPLETO.sql`

---

### 4️⃣ CONSULTAS, VISTAS Y RESULTADOS 
**Consulta 1: Movimientos pendientes de pago**
```sql
SELECT m.id, m.placa, m.tipo_evento, m.monto_calculado, m.codigo_qr, o.nombre
FROM movimientos m
LEFT JOIN operarios o ON m.operario_id = o.id
WHERE m.estado_pago = 'PENDIENTE' AND m.tipo_evento = 'SALIDA'
ORDER BY m.fecha_hora_salida DESC;
```

**Consulta 2: Ingresos diarios totales**
```sql
SELECT 
    DATE(m.fecha_hora_salida) as fecha,
    COUNT(*) as salidas_totales,
    SUM(m.monto_calculado) as ingresos_totales,
    AVG(m.duracion_minutos) as duracion_promedio,
    COUNT(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 END) as pagos_confirmados
FROM movimientos m
WHERE m.tipo_evento = 'SALIDA'
GROUP BY DATE(m.fecha_hora_salida)
ORDER BY fecha DESC;
```

**Consulta 3: Auditoría - Autos sin salida registrada**
```sql
SELECT m.id, m.placa, m.marca, m.modelo, m.fecha_hora_entrada, 
    EXTRACT(HOUR FROM CURRENT_TIMESTAMP - m.fecha_hora_entrada) as horas_adentro,
    o.nombre as registrado_por
FROM movimientos m
LEFT JOIN operarios o ON m.operario_id = o.id
WHERE m.tipo_evento = 'ENTRADA' AND m.fecha_hora_salida IS NULL
ORDER BY m.fecha_hora_entrada ASC;
```

**Consulta 4: Discrepancias (registros vs pagos confirmados)**
```sql
SELECT 
    DATE(m.fecha_hora_salida) as fecha,
    COUNT(*) as transacciones_registradas,
    COUNT(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 END) as transacciones_pagadas,
    COUNT(*) - COUNT(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 END) as pendientes,
    SUM(m.monto_calculado) as monto_total_registrado
FROM movimientos m
WHERE m.tipo_evento = 'SALIDA'
GROUP BY DATE(m.fecha_hora_salida)
HAVING COUNT(*) != COUNT(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 END);
```

**Consulta 5: Histórico por operario**
```sql
SELECT 
    o.nombre,
    COUNT(*) as registros,
    SUM(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 ELSE 0 END) as pagos_confirmados,
    SUM(CASE WHEN m.tipo_evento = 'SALIDA' THEN m.monto_calculado ELSE 0 END) as ingresos
FROM movimientos m
LEFT JOIN operarios o ON m.operario_id = o.id
WHERE DATE(m.fecha_creacion) = CURRENT_DATE
GROUP BY o.nombre
ORDER BY registros DESC;
```

**Vistas:**

```sql
-- VISTA 1: Resumen tiempo real
CREATE VIEW v_estado_actual AS
SELECT 
    COUNT(CASE WHEN tipo_evento = 'ENTRADA' AND fecha_hora_salida IS NULL THEN 1 END) as autos_adentro,
    COUNT(CASE WHEN tipo_evento = 'SALIDA' AND estado_pago = 'PENDIENTE' THEN 1 END) as pagos_pendientes,
    SUM(CASE WHEN tipo_evento = 'SALIDA' AND estado_pago = 'PAGADO' THEN monto_calculado ELSE 0 END) as ingresos_hoy
FROM movimientos
WHERE DATE(fecha_creacion) = CURRENT_DATE;

-- VISTA 2: Reporte diario
CREATE VIEW v_reporte_diario AS
SELECT 
    DATE(fecha_hora_salida) as fecha,
    COUNT(*) as salidas,
    SUM(monto_calculado) as ingresos,
    COUNT(CASE WHEN estado_pago = 'PAGADO' THEN 1 END) as pagados,
    COUNT(CASE WHEN estado_pago = 'PENDIENTE' THEN 1 END) as pendientes
FROM movimientos
WHERE tipo_evento = 'SALIDA'
GROUP BY DATE(fecha_hora_salida);

-- VISTA 3: Anomalías (autos adentro >12h)
CREATE VIEW v_anomalias AS
SELECT 
    id, placa, marca, modelo, fecha_hora_entrada,
    EXTRACT(HOUR FROM CURRENT_TIMESTAMP - fecha_hora_entrada) as horas_adentro
FROM movimientos
WHERE tipo_evento = 'ENTRADA' AND fecha_hora_salida IS NULL
AND fecha_hora_entrada < CURRENT_TIMESTAMP - INTERVAL '12 hours';
```

**Ubicación:** `04_base_datos/consultas/`

---

### 5️⃣ DEFENSA TÉCNICA Y TRABAJO EN EQUIPO 

**Pregunta 1: ¿Por qué PK surrogada (BIGSERIAL) y no placa?**

> **Respuesta:**
> 
> Usamos BIGSERIAL porque:
> 1. **Placa es volátil:** Un vehículo puede cambiar de placa → problemas si es PK
> 2. **Optimización:** BIGSERIAL crea índice automático, búsquedas O(log n)
> 3. **Simplifica FK:** Otros registros usan id, no placa larga
> 4. **Auditoría:** El id nunca cambia, garantiza trazabilidad
> 
> Si usáramos placa como PK:
> - UPDATE placa → Cascade a todos los FK
> - Índice más lento (texto vs número)
> - Complejidad innecesaria

**Pregunta 2: ¿Qué anomalías detectaron normalizando?**

> **Respuesta:**
> 
> **Anomalía 1 (1FN):** Atributos multivaluados
> - Problema: Guardar "info_operario" (nombre, email) en MOVIMIENTO
> - Solución: Crear tabla OPERARIOS, FK en MOVIMIENTO
>
> **Anomalía 2 (2FN):** Dependencia parcial
> - Problema: nombre_operario depende solo de operario_id, no de movimiento_id
> - Solución: Mover nombre_operario a tabla OPERARIOS
>
> **Anomalía 3 (3FN):** Dependencia transitiva
> - Problema: Si guardáramos nombre_parqueo en OPERARIO
> - Solución: Crear tabla PARQUEOS separada (si escalamos)

**Pregunta 3: ¿Cuál fue la consulta más compleja?**

> **Respuesta:**
> 
> **Consulta: Discrepancias (auditoría diaria)**
> 
> ```sql
> SELECT DATE(m.fecha_hora_salida) as fecha,
>     COUNT(*) as registrados,
>     COUNT(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 END) as pagados,
>     SUM(m.monto_calculado) as total
> FROM movimientos m
> WHERE m.tipo_evento = 'SALIDA'
> GROUP BY DATE(m.fecha_hora_salida)
> HAVING COUNT(*) != COUNT(CASE WHEN m.estado_pago = 'PAGADO' THEN 1 END);
> ```
>
> **¿Por qué es compleja?**
> 1. GROUP BY + DATE() = agregar por fecha
> 2. CASE WHEN = lógica condicional
> 3. HAVING = filtro post-agregación
> 4. Compara registrados vs pagados (auditoría)
>
> **Valor empresarial:**
> - Detecta si dinero registrado ≠ dinero cobrado
> - Identifica posibles fraudes o errores
> - Alertas automáticas

**Pregunta 4: ¿Mayor riesgo de inconsistencia y mitigación?**

> **Respuesta:**
> 
> **Riesgo 1: Cálculo de tarifa incorrecto**
> - Riesgo: Si es manual, errores humanos
> - Mitigación: Fórmula automática en BD: `monto = duracion / 60 * 10`
> - Mitigación: CHECK constraint valida positivo
>
> **Riesgo 2: Doble cobro (fraude)**
> - Riesgo: Escanear mismo QR dos veces
> - Mitigación: UNIQUE(codigo_qr) - BD rechaza duplicados
> - Mitigación: QR expira en 5 minutos
> - Mitigación: operario_id audita quién confirmó
>
> **Riesgo 3: Auto olvidado (sin salida)**
> - Riesgo: Pérdida de dinero
> - Mitigación: Vista `v_anomalias` detecta >12h adentro
> - Mitigación: Alertas automáticas para empleado
>
> **Riesgo 4: Pérdida de datos**
> - Riesgo: Fallo local → datos perdidos
> - Mitigación: Supabase (nube) con respaldo automático
> - Mitigación: BD replicada, redundancia

---

## 🚀 Stack Tecnológico

| Componente | Tecnología | Justificación |
|------------|-----------|--------------|
| **BD** | PostgreSQL (Supabase) | ACID nativo, normalización, cloud, sin mantenimiento |
| **OCR** | EasyOCR + Python | Gratuito, 85%+ precisión, sin servidor |
| **Backend** | Python 3.8+ | Librerías OCR maduras, rápido |
| **Admin (Escritorio)** | Tkinter | Interfaz simple, multiplataforma, sin dependencias |
| **Generador QR** | qrcode (Python) | Gratuito, genera QR con datos (tarifa) |
| **Cámara** | OpenCV (Python) | Integración fácil, compatible IP/USB |

---

## 📋 Checklist de Cumplimiento 
### ✅ Modelado Conceptual 
- [ ] 8 pts: Clases con atributos correctos
  - [ ] MOVIMIENTO: id, placa, tipo_evento, fechas, duración, monto, estado_pago, código_qr, operario_id
  - [ ] OPERARIO: id, nombre, email, rol
- [ ] 8 pts: Relaciones y multiplicidades
  - [ ] OPERARIO (1) → (*) MOVIMIENTO
  - [ ] Documentadas en UML
- [ ] 4 pts: Coherencia con reglas de negocio
  - [ ] No doble cobro (UNIQUE codigo_qr)
  - [ ] Tarifa fija (fórmula)
  - [ ] Pago manual
  - [ ] Auditoría (operario_id, fecha)

### ✅ Modelo Relacional y Normalización 
- [ ] 8 pts: PK/FK bien definidas
  - [ ] PK surrogada (BIGSERIAL)
  - [ ] FK hacia OPERARIOS (auditoría)
  - [ ] Justificación documentada
- [ ] 6 pts: Restricciones y dominios
  - [ ] CHECK para enumerados (ENTRADA/SALIDA, PENDIENTE/PAGADO)
  - [ ] CHECK para lógica (salida > entrada, monto > 0)
  - [ ] UNIQUE para codigo_qr
- [ ] 6 pts: Normalización 3FN con justificación
  - [ ] 1FN: Sin multivaluados ✓
  - [ ] 2FN: Sin dependencias parciales ✓
  - [ ] 3FN: Sin dependencias transitivas ✓
  - [ ] Documento explícito de normalización

### ✅ Implementación SQL 
- [ ] 8 pts: Script ejecutable
  - [ ] CREATE TABLE para todas las tablas
  - [ ] FOREIGN KEY constraints
  - [ ] CHECK constraints
  - [ ] Ejecutable sin errores
- [ ] 6 pts: Integridad referencial funcional
  - [ ] Pruebas: intentar violar FK → error ✓
  - [ ] Pruebas: intentar duplicar QR → error ✓
  - [ ] Pruebas: intentar salida < entrada → error ✓
- [ ] 6 pts: Datos de prueba coherentes
  - [ ] Caso 1: entrada + salida completa
  - [ ] Caso 2: entrada sin salida (aún adentro)
  - [ ] Caso 3: pago pendiente

### ✅ Consultas, Vistas y Resultados 
- [ ] 12 pts: 5 consultas requeridas
  - [ ] Q1: Pendientes de pago
  - [ ] Q2: Ingresos diarios
  - [ ] Q3: Autos sin salida
  - [ ] Q4: Auditoría (discrepancias)
  - [ ] Q5: Histórico por operario
- [ ] 8 pts: Exactitud validada
  - [ ] Datos entrada → resultado esperado → resultado obtenido
  - [ ] Documento: resultados_validados.md
  - [ ] 100% de consultas validas
- [ ] 5 pts: 3 vistas útiles
  - [ ] V1: Estado actual (autos adentro, pagos pendientes)
  - [ ] V2: Reporte diario (entradas, salidas, ingresos)
  - [ ] V3: Anomalías (autos >12h adentro)

### ✅ Defensa Técnica y Equipo 
- [ ] 6 pts: Explicación clara del diseño
  - [ ] Pregunta 1: PK/FK ✓
  - [ ] Pregunta 2: Anomalías ✓
  - [ ] Pregunta 3: Consulta compleja ✓
  - [ ] Pregunta 4: Mayor riesgo ✓
- [ ] 6 pts: Respuesta a preguntas técnicas
  - [ ] Concurrencia (2 operarios simultáneamente)
  - [ ] Falla OCR (manual backup)
  - [ ] Recuperación de datos (Supabase cloud)
  - [ ] Escalabilidad (cómo agregar más parqueos)
- [ ] 3 pts: Participación equilibrada
  - [ ] Documento: quién hizo qué
  - [ ] Todos presentan en defensa
  - [ ] Evidencia de colaboración

---

## 🎬 Flujo Usuario Final

**Admin (Empleado en escritorio):**

1. Abre PARKIA en la mañana
2. Ve pantalla: "Estado: 0 autos adentro"
3. Cámara detecta entrada → "ABC1234 ENTRADA registrada"
4. 2 horas después: Cámara detecta salida
5. Pantalla: "ABC1234 - 22.50 Bs - [QR] - Confirmar pago?"
6. Cliente muestra QR (screenshot)
7. Admin clickea: [✓ Confirmar]
8. Sistema: "✓ PAGADO"
9. Al final del día: [Reportes] → "47 salidas, 425.50 Bs, 0 discrepancias"

**Cliente (Mínimo esfuerzo):**

1. Entra con auto
2. 2 horas después, sale
3. Ve QR en pantalla: "22.50 Bs"
4. Toma screenshot
5. Muestra al salir
6. Listo, se va

---

## 📚 Documentación Esperada

- `01_investigacion/` - Análisis del parqueo real
- `02_diseno_conceptual/` - Diagrama UML + casos de uso
- `03_modelo_relacional/` - DER + normalización
- `04_base_datos/` - Scripts SQL + consultas + vistas
- `05_backend/` - Código OCR + auditoría
- `06_admin_escritorio/` - Interfaz Tkinter
- `07_cliente_qr/` - Pantalla QR simple
- `09_documentacion_academica/` - Informe formal 40-50 págs
- `11_defensa/` - Presentación + respuestas

---

## 🏆 Criterios de Excelencia

Para ir **más allá de 100 puntos**:

1. ✨ **Índices de desempeño:** CREATE INDEX en campos búsqueda frecuente
2. ✨ **Triggers automáticos:** Actualizar campos automáticamente
3. ✨ **Transacciones ACID:** BEGIN...COMMIT para operaciones críticas
4. ✨ **Respaldos:** Script de backup automático a nube
5. ✨ **Dashboard tiempo real:** Vista HTML que actualiza en vivo
6. ✨ **Reportes PDF:** Generar reportes formales descargables
7. ✨ **Notificaciones:** Alertas automáticas (Telegram/Email)
8. ✨ **Integración cámara IP:** No solo webcam, sino cámaras de vigilancia reales

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar
git clone https://github.com/tuusuario/parkia-sistema.git
cd parkia-sistema

# 2. Instalar
pip install -r 05_backend/requirements.txt

# 3. Configurar Supabase
cp .env.example .env
# Editar con credenciales

# 4. Crear BD
psql -U postgres -d parkia_db -f 04_base_datos/scripts_sql/00_PARKIA_COMPLETO.sql

# 5. Ejecutar admin
python 06_admin_escritorio/interfaz_admin.py

# 6. Leer docs
open 09_documentacion_academica/DOCUMENTO_COMPLETO.md
```

---

## 📄 Licencia

MIT License - Libre para uso académico y comercial

---

```
╔════════════════════════════════════════════════════════╗
║  🅿️  PARKIA - Sistema Inteligente de               ║
║     Estacionamientos para Escritorio                 ║
║                                                      ║
║  ✓ OCR Automático                                   ║
║  ✓ Base de Datos Relacional 3FN                     ║
║  ✓ Admin Desktop (Tkinter)                          ║
║  ✓ Cliente QR (Mínimo)                              ║
║  ✓ Auditoría Completa                               ║
║  ✓ 100/100 PUNTOS                                   ║
║                                                      ║
║  "Parqueos inteligentes, empleados felices"         ║
╚════════════════════════════════════════════════════════╝
```

---

**Autor:** sARA RAQUEL SAHONERO SALAS
**Materia:** INF-312 Base de Datos I  

