import streamlit as st
import joblib

# Áreas del CASM-83
areas = [
    'CCFM', 'CCSS', 'CCNA', 'CCCO', 'ARTE', 'BURO',
    'CCEP', 'IIAA', 'FINA', 'LING', 'JURI'
]

carreras_por_area = {
    "CCFM": [
        "Ingenierías: Civil, de Sistemas, Industrial, Electrónica, de Minas, Sanitaria, Textil, Química, Mecánica (eléctrica y de fluidos), Telecomunicaciones, de Sonido, Metalurgia.",
        "Arquitectura", "Matemáticas", "Física", "Meteorología", "Geografía", "Geología",
        "Técnicos relacionados: Técnico en TV y radio, electricista, mecánico automotriz, mecánico de banco, mecánica de aviones, construcción civil, impresor, linotipista, topografía, computación e informática, ensamblaje, mantenimiento y reparación de computadoras, operador técnico de radio y televisión."
    ],
    "CCSS": [
        "Antropología", "Sociología", "Trabajo Social", "Historia", "Arqueología", "Filosofía",
        "Teología", "Psicología", "Auxiliar de educación"
    ],
    "CCNA": [
        "Medicina Humana", "Obstetricia", "Enfermería", "Nutrición", "Biología", "Odontología",
        "Químico - Farmacéutico", "Medicina Veterinaria", "Agronomía", "Zootecnia", "Psicología",
        "Industrias Alimentarias", "Geografía"
    ],
    "CCCO": [
        "Ciencias de la Comunicación", "Periodismo", "Publicidad", "Comunicación audiovisual (cine, radio y televisión)",
        "Relaciones Públicas", "Técnico en TV y radio", "Visitador médico", "Guía turístico", "Promotores de turismo"
    ],
    "ARTE": [
        "Artesanías en cerámica, cueros, tejido, etc.", "Pintor", "Actor", "Escultor", "Decorador",
        "Diseñador de modas", "Director de cine y televisión", "Músico", "Profesor de música",
        "Crítico musical", "Arquitectura", "Técnico en dibujo lineal", "Publicitario", "Ebanistería",
        "Decoración de interiores", "Conservación y restauración", "Fotografía profesional", "Fotografía"
    ],
    "BURO": [
        "Empleado de oficina", "Bibliotecario", "Secretario(a): ejecutivo, bilingüe, aerocomercial, computarizado, médico",
        "Archivero", "Bibliotecología y Ciencias de la Información"
    ],
    "CCEP": [
        "Economista", "Estadista", "Político Diplomático", "Administrador de empresas: hotelera, turismo, comercio nacional e internacional",
        "Marketing", "Visitador médico", "Escritor", "Lingüista", "Traductor e intérprete de idiomas"
    ],
    "IIAA": [
        "Oficial del Ejército", "Oficial de la Fuerza Aérea del Perú (FAP)", "Oficial de la Marina", "Oficial de la Policía", "CITEN", "ETE"
    ],
    "FINA": [
        "Contabilidad", "Finanzas", "Banca y seguros", "Auxiliar de contabilidad", "Bancario", "Secretario contable", "Vendedor"
    ],
    "LING": [
        "Escritor", "Lingüista", "Traductor e intérprete de idiomas", "Secretario bilingüe"
    ],
    "JURI": [
        "Derecho: Penal, Civil, Laboral", "Notario público", "Escribano", "Secretario legal"
    ]
}

# Índices columna (letra "a")
column_items = {}
for idx, area in enumerate(areas):
    items = [idx + 13 * i for i in range(11)]  # p1 index 0, p14 index 13, etc.
    column_items[area] = items

# Índices fila (letra "b")
row_items = {}
for idx, area in enumerate(areas):
    start = idx * 11
    end = start + 11
    items = list(range(start, end))
    row_items[area] = items

# Función para calcular puntajes directos
def calcular_puntajes_directos(respuestas):
    puntajes = []
    for area in areas:
        a_count = sum(respuestas[i] == 'a' or respuestas[i] == 'ambas' for i in column_items[area])
        b_count = sum(respuestas[i] == 'b' or respuestas[i] == 'ambas' for i in row_items[area])
        puntajes.append(a_count + b_count)
    return puntajes

preguntas = [
    "a) Le gusta resolver problemas de matemáticas; o\n b) Prefiere diseñar el modelo de casas, edificios, parques, etc.",
    "a) Le agrada observar la conducta de las personas y opinar sobre su personalidad; \nb) Prefiere expresar un fenómeno concreto en una ecuación matemática.",
    "a) Le gusta caminar por los cerros buscando piedras raras; \nb) Prefiere diseñar las viviendas de una urbanización.",
    "a) Le gusta escribir artículos deportivos para un diario; \nb) Prefiere determinar la resistencia de materiales para una construcción.",
    "a) Le gusta hacer tallado en madera; \nb) Prefiere calcular la cantidad de materiales para una construcción.",
    "a) Le gusta ordenar y archivar documentos; \nb) Prefiere proyectar el sistema eléctrico de una construcción.",
    "a) Le agrada dedicar su tiempo en el estudio de teorías económicas; \nb) Prefiere dedicar su tiempo en la lectura de revistas sobre mecánica.",
    "a) Le gusta mucha la vida militar; \nb) Prefiere diseñar máquinas, motores, etc., de alto rendimiento.",
    "a) Le gusta planificar acerca de cómo formar una cooperativa; \nb) Prefiere estudiar el lenguaje de computación (IBM).",
    "a) Le agrada estudiar la gramática; \nb) Prefiere estudiar las matemáticas.",
    "a) Le interesa mucho ser abogado; \nb) Preferiría dedicarse a escribir un tratado de Física-Matemáticas.",
    "a) Le cuenta a su padre y a su madre todas sus cosas; \nb) Prefiere ocultar algunas cosas para usted solo(a).",
    "a) Le agrada estudiar la estructura anatómica de los cuerpos; \nb) Prefiere asumir la defensa legal de una persona acusada por algún delito.",
    "a) Le interesa mucho estudiar cómo funciona un computador; \nb) Prefiere el estudio de las leyes y principios de la conducta psicológica.",
    "a) Le agrada analizar la forma como se organiza un pueblo; \nb) Prefiere responderse a la pregunta del ¿Por qué de los seres y de las cosas?",
    "a) Le gusta analizar las rocas, piedras y tierra para averiguar su composición mineral; \nb) Prefiere el estudio de las organizaciones sean: campesinas, educativas, laborales, políticas, económicas o religiosas.",
    "a) Le gusta escribir artículos culturales para un diario; \nb) Prefiere pensar largamente acerca de la forma como el hombre podría mejorar su existencia.",
    "a) Le agrada diseñar muebles, puertas, ventanas, etc.; \nb) Prefiere dedicar su tiempo en conocer las costumbres y tradicionales de los pueblos.",
    "a) Le interesa mucho conocer el trámite documentario de un ministerio público; \nb) Prefiere el estudio de las religiones.",
    "a) Le interesa mucho conocer los mecanismos de la economía nacional; \nb) Prefiere ser guía espiritual de las personas.",
    "a) Le gusta ser parte de la administración de una cooperativa; \nb) Prefiere el estudio de las formas más efectivas para la enseñanza de jóvenes y niños.",
    "a) Le interesa mucho investigar la raíz gramatical de las palabras de su idioma; \nb) Prefiere dedicar su tiempo en la búsqueda de huacos y ruinas.",
    "a) Le agrada mucho estudiar el código del derecho civil; \nb) Prefiere el estudio de las culturas peruanas y de otras naciones.",
    "a) Le agrada que sus hermanos o familiares lo vigilen constantemente; \nb) Prefiere que confíen en su buen criterio.",
    "a) Le gustaría escribir un tratado acerca de la Historia del Perú; \nb) Prefiere asumir la defensa legal de un acusado por narcotráfico.",
    "a) Le gusta proyectar las redes de agua y desagüe de una ciudad; \nb) Prefiere estudiar acerca de las enfermedades de la dentadura.",
    "a) Le gusta visitar museos arqueológicos y conocer la vivienda y otros utensilios de nuestros antepasados; \nb) Prefiere hacer moldes para una dentadura postiza.",
    "a) Le gusta recolectar plantas y clasificarlas por especie; \nb) Prefiere leer sobre el origen y funcionamiento de las plantas y animales.",
    "a) Le gusta saber cómo se organiza una editorial periodística; \nb) Prefiere conocer las características de los órganos humanos y cómo funcionan.",
    "a) Le agrada construir muebles, puertas, ventanas, etc.; \nb) Prefiere estudiar acerca de las enfermedades de las personas.",
    "a) Le agradaría trabajar en la recepción y trámite documentario de una oficina pública; \nb) Prefiere experimentar con las plantas para obtener una nueva especie.",
    "a) Le gusta proyectar los mecanismos de inversión económica de una empresa; \nb) Prefiere analizar las tierras para obtener mayor producción agropecuaria.",
    "a) Le agrada recibir y ejecutar órdenes de un superior; \nb) Prefiere el estudio de los órganos de los animales y su funcionamiento.",
    "a) Le gusta saber mucho sobre los principios económicos de una cooperativa; \nb) Prefiere conocer las enfermedades que aquejan, sea el ganado, aves, perros, etc.",
    "a) Le agrada estudiar los fonemas (sonidos verbales) de su idioma, o de otros; \nb) Prefiere dedicar mucho tiempo en el estudio de la química.",
    "a) Le agrada defender pleitos judiciales de recuperación de tierras; \nb) Prefiere hacer mezclas de sustancias químicas para obtener derivados con fines productivos.",
    "a) Sus amigos saben todo de usted, para ellos no tiene secretos; \nb) Prefiere reservar algo para usted solo(a) algunos secretos.",
    "a) Le gusta investigar acerca de los recursos naturales de nuestro país (su fauna, su flora y su suelo); \nb) Prefiere estudiar derecho internacional.",
    "a) Le gusta desarrollar programas de computación para proveer de información rápida y eficiente a una empresa, institución, etc.; \nb) Prefiere obtener fotografías que hagan noticias.",
    "a) Le gusta mucho conocer el problema de las personas que y tramitar su solución; \nb) Prefiere dedicar su tiempo en la búsqueda de personajes que hacen noticia.",
    "a) Le gusta estudiar las características territoriales de los continentes; \nb) Prefiere entrevistar a políticos con el propósito de establecer su posición frente a un problema.",
    "a) Le gusta conocer el funcionamiento de las máquinas impresoras de periódicos; \nb) Prefiere trabajar en el montaje fotográfico de un diario o revista.",
    "a) Le gusta proyectar el tipo de muebles, cortinas y adornos sea para una oficina o para un hogar; \nb) Prefiere trabajar como redactor en un diario o revista.",
    "a) Le gusta redactar cartas comerciales, al igual que oficios y solicitudes; \nb) Prefiere averiguar lo que opina el público respecto a un producto.",
    "a) Le gusta estudiar las leyes de la oferta y demanda; \nb) Prefiere redactar el tema para un anuncio publicitario.",
    "a) Le gusta organizar el servicio de inteligencia de un cuartel; \nb) Prefiere trabajar en una agencia de publicidad.",
    "a) Le gusta trabajar buscando casas de alquiler para ofrecerlas al público; \nb) Prefiere estudiar las características psicológicas para lograr un buen impacto publicitario.",
    "a) Le interesa investigar acerca de cómo se originaron los idiomas; \nb) Prefiere preparar y ejecutar encuestas para conocer la opinión de las personas.",
    "a) Le agrada hacer los trámites legales de un juicio de divorcio; \nb) Prefiere trabajar estableciendo contactos entre una empresa y otra.",
    "a) Cuando está dando un examen y tiene la oportunidad de verificar una respuesta, nunca lo hace; \nb) Prefiere aprovechar la seguridad que la ocasión le confiere.",
    "a) Le interesa investigar sobre los problemas del lenguaje en la comunicación masiva; \nb) Prefiere redactar documentos legales para contratos internacionales.",
    "a) Le gusta trabajar haciendo instalaciones eléctricas; \nb) Prefiere dedicar su tiempo en la lectura de las novedades en la decoración de ambientes.",
    "a) Le agrada mucho visitar el hogar de los trabajadores con el fin de verificar su verdadera situación social y económica; \nb) Prefiere trabajar en el decorado de tiendas y vitrinas.",
    "a) Le gusta estudiar los recursos geográficos; \nb) Prefiere observar el comportamiento de las personas e imitarlas.",
    "a) Le gusta dedicar su tiempo a la organización de eventos deportivos entre dos o más centros laborales; \nb) Prefiere dedicarse al estudio de la vida y obra de los grandes actores del cine y del teatro.",
    "a) Le gusta la idea de estudiar escultura en la escuela de bellas artes; \nb) Le atrae ser parte de un elenco de teatro.",
    "a) Le gusta trabajar de mecanógrafo; \nb) Le gusta más dar forma a objetos moldeables, sea plastilina, migas, arcilla, piedras, etc.",
    "a) Le agrada mucho estudiar los fundamentos por los que una moneda se devalúa; \nb) Prefiere la lectura acerca de la vida y obra de grandes escultores como Miguel Ángel, Leonardo Da Vinci, etc.",
    "a) Le agrada mucho la vida del marinero; \nb) Prefiere combinar colores para expresar con naturalidad y belleza un rostro o un paisaje.",
    "a) Encuentra atractivo trabajar tramitando la compra-venta de inmuebles; \nb) Prefiere utilizar las líneas y colores para expresar un sentimiento.",
    "a) Le agrada estudiar las lenguas y dialectos aborígenes; \nb) Prefiere combinar sonidos para obtener una nueva música.",
    "a) Le agrada tramitar judicialmente el reconocimiento de hijos; \nb) Le agrada más aprender o tocar algún instrumento musical.",
    "a) Si pasa por un cine y descubre que no hay vigilancia, no se aprovecha de la situación; \nb) Prefiere aprovechar la ocasión para ingresar sin pagar su boleto.",
    "a) Le interesa más diseñar y/o confeccionar artículos de cuero; \nb) Prefiere asumir la defensa legal en la demarcación de fronteras territoriales.",
    "a) Prefiere estudiar acerca de cómo la energía se transforma en imágenes de TV, radio, etc.; \nb) Le gusta tomar apuntes textuales o dictados de otras personas.",
    "a) Le gusta leer sobre la vida y obra de los santos religiosos; \nb) Prefiere hacer catálogos o listados de los libros de una biblioteca.",
    "a) Le gusta dedicar mucho de su tiempo en la lectura de astronomía; \nb) Prefiere trabajar clasificando los libros por autores.",
    "a) Le gusta trabajar difundiendo el prestigio de su centro laboral; \nb) Prefiere trabajar recibiendo y entregando documentos valorados como cheques, giros, libretas de ahorro, etc.",
    "a) Le interesa mucho leer sobre la vida y obra de músicos famosos; \nb) Prefiere el tipo de trabajo de un empleado bancario.",
    "a) Le interesa mucho conseguir un trabajo en un banco comercial; \nb) Prefiere dedicarse a clasificar libros por especialidades.",
    "a) Le gusta dedicar su tiempo en el conocimiento del por qué ocurre la inflación económica; \nb) Prefiere dedicarse al estudio de cómo se organiza una biblioteca.",
    "a) Le interesa mucho el conocimiento de la organización de un buque de guerra; \nb) Prefiere dedicarse a la recepción y comunicación de mensajes sean verbales o por escrito.",
    "a) Le gusta trabajar tramitando la compra-venta de vehículos motorizados; \nb) Prefiere transcribir los documentos de la administración pública.",
    "a) Le gusta dedicar gran parte de su tiempo al estudio de las normas y reglas para el uso adecuado del lenguaje; \nb) Prefiere trabajar como secretario adjunto al jefe.",
    "a) Le gusta dedicar su tiempo planteando la defensa de un juicio de alquiler; \nb) Prefiere asesorar y aconsejar en torno a trámites documentarios.",
    "a) Si en la calle se encuentra dinero, sin documento alguno acude a la radio o TV para buscar al infortunado; \nb) Preferiría quedarse con el dinero, pues no se conoce el dueño.",
    "a) Le interesa trabajar en la implementación de bibliotecas distritales; \nb) Prefiere asumir la responsabilidad legal para que un fugitivo, con residencia en otro país, sea devuelto a su país.",
    "a) Le gusta estudiar acerca de cómo la energía se transforma en movimiento; \nb) Preferiría hacer una tesis sobre el manejo económico para el país.",
    "a) Le agrada leer sobre la vida y obra de grandes personajes de educación, sean: profesores, filósofos, psicológicos; \nb) Prefiere estudiar acerca de las bases económicas de un país.",
    "a) Le gusta estudiar los astros; sus características, origen y evolución; \nb) Prefiere establecer comparaciones entre los sistemas y modelos económicos del mundo.",
    "a) Le interesa trabajar exclusivamente promocionando la imagen de su centro laboral; \nb) Prefiere estudiar las grandes corrientes ideológicas del mundo.",
    "a) Le gusta y practica el baile como expresión artística; \nb) Prefiere estudiar las bases de la organización política del Tahuantinsuyo.",
    "a) Le gusta mucho saber sobre el manejo de los archivos públicos; \nb) Prefiere establecer diferencias entre los distintos modelos políticos.",
    "a) Le gusta investigar sobre las características de los regímenes totalitarios, democráticos, republicanos, etc.; \nb) Prefiere ser el representante de su país en el extranjero.",
    "a) Le gusta ser capitán de un buque de guerra; \nb) Le interesa más formar parte y conducir grupos con fines políticos.",
    "a) Le agrada ser visitador médico; \nb) Prefiere dedicar su tiempo en la lectura de la vida y obra de los grandes políticos.",
    "a) Siente placer buscando en el diccionario el significado de palabras nuevas; \nb) Prefiere dedicar todo su tiempo en aras de la paz entre las naciones.",
    "a) Le interesa mucho estudiar el código penal; \nb) Prefiere estudiar los sistemas políticos de otros países.",
    "a) Le agrada que le dejen muchas tareas para su casa; \nb) Prefiere que estas sean lo necesario para aprender.",
    "a) Le agrada ser miembro activo de una agrupación política; \nb) Prefiere escuchar acusaciones y defensas para sancionar de acuerdo a lo que la ley señala.",
    "a) Le gusta hacer los cálculos para el diseño de las telas a gran escala; \nb) Le interesa más la mecánica de los barcos y submarinos.",
    "a) Le agrada observar y evaluar cómo se desarrolla la inteligencia y personalidad; \nb) Prefiere ser aviador.",
    "a) Le gustaría dedicar su tiempo en el descubrimiento de nuevos medicamentos; \nb) Prefiere dedicarse a la lectura de la vida y obra de reconocidos militares, que han aportado en la organización de su institución.",
    "a) Le gusta la aventura cuando está dirigida a descubrir algo que haga noticia; \nb) Prefiere conocer el mecanismo de los aviones de guerra.",
    "a) Le gusta ser parte de una agrupación de baile y danza; \nb) Preferiría pertenecer a la Fuerza Aérea.",
    "a) Le gusta la idea de trabajo de llevar mensajes de una dependencia a otra; \nb) Prefiere ser miembro de la policía.",
    "a) Le gustaría trabajar estableciendo vínculos culturales con otros países; \nb) Prefiere el trabajo en la detección y comprobación del delito.",
    "a) Le gusta trabajar custodiando el orden público; \nb) Le gusta ser vigilante receloso de nuestras fronteras.",
    "a) Le gusta persuadir a los boticarios en la compra de nuevos medicamentos; \nb) Prefiere trabajar vigilando a los presos en las prisiones.",
    "a) Le apasiona leer obras de escritores serios y famosos; \nb) Prefiere organizar el servicio de inteligencia en la destrucción del narcotráfico.",
    "a) Le gusta asumir la defensa legal de una persona acusada de robo; \nb) Prefiere conocer el mecanismo de las armas de fuego.",
    "a) Se aleja Ud. cuando sus amistades cuentan “chistes colorados”; \nb) Prefiere quedarse gozando de la ocasión.",
    "a) Le interesa mucho saber cómo se organiza un ejército; \nb) Prefiere participar como jurado de un juicio.",
    "a) Le gusta proyectar la extracción de metales de una mina; \nb) Prefiere estudiar el nombre de los medicamentos y su ventaja comercial.",
    "a) Le gusta descifrar los diseños gráficos y escritos de culturas muy antiguas; \nb) Prefiere persuadir a la gente para que compre un producto.",
    "a) Le agrada el estudio de los mecanismos de la visión y de sus enfermedades; \nb) Prefiere vender cosas.",
    "a) Le gustaría ganarse la vida escribiendo para un diario o revista; \nb) Prefiere estudiar el mercado y descubrir el producto de mayor demanda.",
    "a) Le gusta actuar, representando a distintos personajes; \nb) Le agrada más tener su propio negocio.",
    "a) Le gusta sentirse importante sabiendo que de Ud. depende la rapidez o la lentitud de una solicitud; \nb) Prefiere trabajar en un bazar.",
    "a) Le gusta planificar sea para una empresa local o a nivel nacional; \nb) Prefiere el negocio de una bodega o tienda de abarrotes.",
    "a) Le interesa mucho utilizar sus conocimientos en la construcción de armamentos; \nb) Prefiere organizar empresas de finanzas y comercio.",
    "a) Le agrada llevar la contabilidad de una empresa o negocio; \nb) Prefiere hacer las planillas de pago para los trabajadores de una empresa o institución.",
    "a) Le agrada escribir cartas y luego hacer tantas correcciones como sean necesarias; \nb) Prefiere ser incorporado como miembro de la corporación nacional de comercio.",
    "a) Le gusta asumir la defensa legal de una persona acusada de asesinato; \nb) Prefiere ser incorporado como miembro de la corporación nacional de comercio.",
    "a) Le agrada vestir todos los días muy formalmente (con terno y corbata por ejemplo); \nb) Prefiere reservar esa vestimenta para ciertas ocasiones.",
    "a) Le gusta evaluar la producción laboral de un grupo de trabajadores; \nb) Prefiere plantear, previa investigación, la acusación de un sujeto que ha actuado en contra la ley.",
    "a) Le gusta estudiar acerca de los reactores atómicos; \nb) Prefiere el estudio de las distintas formas literarias.",
    "a) Le agrada investigar en torno a la problemática social del Perú; \nb) Prefiere escribir, cuidando mucho ser comprendido, al tiempo que sus escritos resulten agradables al lector.",
    "a) Le gustaría escribir un tratado sobre anatomía humana; \nb) Prefiere recitar sus propios poemas.",
    "a) Le gustaría incorporarse al Colegio de Periodistas del Perú; \nb) Prefiere aprender otro idioma.",
    "a) Le gusta diseñar y/o confeccionar: adornos, utensilios, etc., en cerámica, vidrio, etc.; \nb) Prefiere traducir textos escritos en otros idiomas.",
    "a) Le gustaría desarrollar técnicas de mayor eficiencia en el trámite documentario de un ministerio público; \nb) Prefiere escribir en otro idioma.",
    "a) Le agradaría mucho ser el secretario general de una central sindical; \nb) Prefiere dedicar su tiempo al estudio de lenguas extintas (muertas).",
    "a) Le gustaría dedicarse al estudio de armas de alta peligrosidad; \nb) Prefiere trabajar como traductor.",
    "a) Le gusta llevar las estadísticas de ingresos y egresos mensuales de una empresa o tal vez de una nación; \nb) Prefiere los cursos de idiomas: inglés, francés, italiano, etc.",
    "a) Le gusta ser incorporado como miembro de la Academia de la Lengua Española; \nb) Prefiere ser incorporado al Instituto Nacional del Idioma.",
    "a) Le interesaría ser el asesor legal de un ministro de Estado; \nb) Prefiere aquellas situaciones que le inspiran a escribir.",
    "a) Nunca ha bebido licor, aún en ciertas ocasiones lo ha rechazado; \nb) Por lo contrario, se ha adecuado a las circunstancias.",
    "a) Le agrada dedicar mucho su tiempo en la escritura de poemas, cuentos; \nb) Prefiere sentirse importante al saber que de su defensa legal depende la libertad de una persona.",
    "a) Le agrada estudiar la estructura atómica de los cuerpos; \nb) Prefiere asumir la defensa legal de una persona acusada por algún delito.",
    "a) Le gustaría escribir un tratado acerca de la Historia del Perú; \nb) Prefiere asumir la defensa legal de un acusado por narcotráfico.",
    "a) Le gusta investigar acerca de los recursos naturales de nuestro país (su fauna, su flora y suelo); \nb) Prefiere estudiar el derecho internacional.",
    "a) Le interesa investigar sobre los problemas de lenguaje en la comunicación masiva; \nb) Prefiere redactar documentos legales para contratos internacionales.",
    "a) Le interesa diseñar y/o confeccionar artículos de cuero; \nb) Prefiere asumir la defensa legal en la demarcación de fronteras territoriales.",
    "a) Le interesa trabajar en la implementación de bibliotecas distritales; \nb) Prefiere asumir la responsabilidad legal para que un fugitivo con residencia en otro país sea devuelto a su país.",
    "a) Le agrada ser miembro activo de una agrupación política; \nb) Prefiere escuchar acusaciones y defensas, para sancionar de acuerdo a lo que la ley señala.",
    "a) Le interesa mucho saber cómo se organiza un ejército; \nb) Prefiere participar como jurado en un juicio.",
    "a) Le gusta evaluar la producción laboral de un grupo de trabajadores; \nb) Prefiere plantear previa investigación la acusación de un sujeto que ha ido en contra de la ley.",
    "a) Le gusta dedicar mucho su tiempo en la escritura de poemas, cuentos; \nb) Prefiere sentirse importante al saber que de su defensa legal depende la libertad de una persona.",
    "a) Le gustaría dedicarse a la legalización de documentos (contratos, cartas, partidas, títulos, etc.); \nb) Prefiere ser incorporado en una comisión para redactar un proyecto de ley.",
    "a) Le agrada viajar en un microbús repleto de gente aun cuando no tiene ningún apuro; \nb) Prefiere esperar otro vehículo.",
    "a) Le gusta resolver problemas matemáticos; \nb) Prefiere diseñar el modelo de casas, edificios, parques, etc."
]

# --- Interfaz Streamlit ---
st.title("Career Guidance Test with Machine Learning")

respuestas = []

cols_por_fila = 5  # número de columnas (preguntas) por fila

for i in range(0, len(preguntas), cols_por_fila):
    cols = st.columns(cols_por_fila)
    for j in range(cols_por_fila):
        idx = i + j
        if idx < len(preguntas):
            with cols[j]:
                st.markdown(f"<b>{idx + 1}.</b> {preguntas[idx].replace(';', '').replace('\n', '<br>')}", unsafe_allow_html=True)
                respuesta = st.radio(
                    label="",
                    options=['a', 'b', 'ambas'],
                    key=f"preg_{idx + 1}"
                )
                respuestas.append(respuesta)
                st.markdown("<br>", unsafe_allow_html=True)  # espacio vertical

# Botón de predicción
if st.button("Predecir perfil vocacional"):
    if len(respuestas) == len(preguntas):
        puntajes = calcular_puntajes_directos(respuestas)
        modelo = joblib.load('modelo_rf.pkl')
        le = joblib.load('label_encoder.pkl')
        area_predicha = le.inverse_transform(modelo.predict([puntajes]))[0]

        st.success(f"Área vocacional dominante predicha por el modelo: **{area_predicha}**")
        st.write("Puntajes directos usados:", dict(zip(areas, puntajes)))

        # Mostrar carreras sugeridas
        if area_predicha in carreras_por_area:
           
            st.subheader("Carreras recomendadas según tu perfil vocacional:")
            for carrera in carreras_por_area[area_predicha]:
                st.markdown(f"- {carrera}")
        else:
            st.warning("No se encontraron carreras asociadas a esta área.")

        # Recomendación final reflexiva
        st.markdown("---")
        st.markdown(
            """
            <div style='background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #3498db;'>
                <h4>🔍 Recomendación final</h4>
                <p style='font-size: 16px;'>
                    Este resultado representa una orientación basada en tus intereses actuales y no debe considerarse una decisión definitiva. 
                    La elección de una carrera profesional es un proceso personal que debe considerar no solo tus habilidades e inclinaciones, 
                    sino también tus metas, valores y aspiraciones a largo plazo.
                </p>
                <p style='font-size: 16px;'>
                    Si el área sugerida coincide con lo que te motiva, puedes tomarlo como una confirmación. 
                    Pero si no, recuerda que lo más importante es construir un camino con sentido, compromiso y pasión.
                </p>
                <p><i>“No preguntes qué necesita el mundo. Pregúntate qué te hace sentir vivo, y ve y haz eso. Porque lo que el mundo necesita es gente que se sienta viva”.<br>– Howard Thurman</i></p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Por favor, responde todas las preguntas antes de predecir.")
