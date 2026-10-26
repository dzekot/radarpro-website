"""Generate the localized guide pages from one structural template.

Each locale keeps the same section order and anchors as radar-guide.html so the
hreflang set stays consistent, but the copy is written for that market instead of
being a literal translation: EDS is explained as a Türkiye-specific term, and the
"official service" section talks about the reader's own authority rather than the
Turkish Ministry.
"""

import io
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
SITE = "https://radarpro.online"

APP_STORE = "https://apps.apple.com/de/app/radarpro-radar-eds/id6776351434"
PLAY_STORE = "https://play.google.com/store/apps/details?id=com.radartr.radarpro"

GUIDES = {
    "tr": "radar-rehberi.html",
    "en": "radar-guide.html",
    "es": "guide-es.html",
    "de": "guide-de.html",
    "ru": "guide-ru.html",
    "ar": "guide-ar.html",
    "pt": "guide-pt.html",
}

NAV_LABEL = {
    "tr": "TR",
    "en": "EN",
    "es": "ES",
    "de": "DE",
    "ru": "RU",
    "ar": "AR",
    "pt": "PT",
}

NAV_TITLE = {
    "tr": "Türkçe",
    "en": "English",
    "es": "Español",
    "de": "Deutsch",
    "ru": "Русский",
    "ar": "العربية",
    "pt": "Português",
}

CONTENT = {
    "es": {
        "lang_attr": "es",
        "dir": "ltr",
        "file": "guide-es.html",
        "title": "Guía de radares, cámaras y tramos de velocidad media | RadarPro",
        "desc": "Qué avisa RadarPro, cómo funcionan los radares fijos, las cámaras de semáforo y los tramos de velocidad media, y dónde terminan los datos.",
        "skip": "Ir al contenido",
        "contents_label": "Guía de radares y velocidad media",
        "h1": "Radares, cámaras y tramos de velocidad media",
        "intro": "Antes de salir conviene saber qué te dice un aviso y hasta dónde llega su dato. RadarPro es una app independiente de concienciación al conducir, con avisos por voz para los puntos de su base de datos.",
        "tiers": "Dentro de la misma app RadarPro, la versión gratuita incluye el mapa, los puntos de radares, los avisos en primer plano y las actualizaciones manuales de datos. Pro añade avisos en segundo plano, actualizaciones automáticas y detección de conducción con los permisos necesarios.",
        "sections": [
            (
                "avisos",
                "¿Cómo funcionan los avisos de radares?",
                "RadarPro compara tu posición con los puntos de radar y control de su base de datos y, al acercarte, anuncia por voz la distancia y, cuando está disponible, el límite de velocidad. El mapa, los avisos en primer plano y las actualizaciones manuales siguen disponibles en la versión gratuita. La distancia del aviso y la cobertura dependen del tipo de punto, de los datos disponibles y de la precisión de la ubicación.",
            ),
            (
                "servicio-oficial",
                "¿Es RadarPro un servicio oficial de tráfico?",
                "No. RadarPro es independiente y no es una aplicación oficial de ninguna autoridad de tráfico, ni mantiene vínculo con ella. La información publicada por la autoridad de tu país y la señalización en la vía siempre tienen prioridad.",
            ),
            (
                "eds-velocidad-media",
                "¿Qué diferencia hay entre EDS y un tramo de velocidad media?",
                "EDS es el nombre que reciben en Turquía los sistemas electrónicos de control del tráfico. En un tramo de velocidad media se mide la velocidad a partir de la distancia y el tiempo entre la entrada y la salida. RadarPro ofrece avisos de entrada, velocidad media dentro del tramo y salida en los tramos compatibles. El límite aplicable lo determinan las señales y las normas de tráfico.",
            ),
            (
                "segundo-plano",
                "¿Funcionan los avisos con otra app de navegación abierta?",
                "Pro incluye avisos por voz en segundo plano con los permisos de ubicación y audio necesarios. En la versión gratuita los avisos funcionan con RadarPro en primer plano. Los usuarios nuevos que cumplan los requisitos también pueden probar los avisos en segundo plano en una experiencia inicial de una sola vez. El sistema operativo, el ahorro de energía, la salida de audio y los permisos pueden afectar a los avisos.",
            ),
            (
                "datos",
                "¿Cómo se gestionan las cámaras nuevas y las actualizaciones?",
                "RadarPro utiliza su base de datos existente; una cámara recién instalada, trasladada o retirada puede no aparecer todavía. Los usuarios gratuitos pueden actualizar manualmente. Pro incluye actualizaciones automáticas cuando hay conexión y una actualización publicada. El mapa no es una lista completa ni siempre actualizada de todas las cámaras del mundo.",
            ),
            (
                "inicio-y-prueba",
                "¿La experiencia inicial es lo mismo que la prueba de la suscripción Pro?",
                "No. En la experiencia inicial de un usuario nuevo que cumpla los requisitos, el umbral de evaluación son tres anuncios de radar/EDS en segundo plano distintos que terminen de reproducirse; esa experiencia no inicia una suscripción. La prueba de 14 días de la tienda es distinta y puede ofrecerse con una oferta anual de Pro elegible. Consulta en la pantalla de compra la elegibilidad, la renovación y el precio.",
            ),
            (
                "seguridad",
                "¿Usar RadarPro significa que no me multarán?",
                "No. RadarPro es una ayuda a la concienciación al conducir. Respeta los límites de velocidad y las normas locales, y no mires la pantalla ni un proceso de compra mientras conduces. Los datos, la ubicación y las condiciones del dispositivo impiden garantizar un aviso para cada cámara en cualquier situación.",
            ),
        ],
        "download_h2": "Usa RadarPro en iOS o Android",
        "download_p": "Empieza con el mapa gratuito y los avisos en primer plano. Consulta las ofertas Pro, los precios locales y las condiciones de prueba en la pantalla de compra dentro de la app.",
        "store_primary": "Descargar en el App Store",
        "store_secondary": "Disponible en Google Play",
        "footer_experience": "Experiencia de conducción",
        "footer_privacy": "Política de privacidad (inglés)",
        "footer_terms": "Condiciones de uso (inglés)",
    },
    "de": {
        "lang_attr": "de",
        "dir": "ltr",
        "file": "guide-de.html",
        "title": "Ratgeber: Blitzer, EDS und Abschnittskontrolle | RadarPro",
        "desc": "Was RadarPro meldet, wie feste Blitzer, Rotlichtkameras und Abschnittskontrollen funktionieren und wo die Daten enden.",
        "skip": "Zum Inhalt springen",
        "contents_label": "Ratgeber zu Radar und Geschwindigkeit",
        "h1": "Blitzer, EDS und Abschnittskontrolle",
        "intro": "Vor der Fahrt lohnt es sich zu wissen, was eine Warnung aussagt und wo ihre Daten enden. RadarPro ist eine unabhängige Fahrassistenz-App mit Sprachwarnungen für die Punkte ihrer Datenbank.",
        "tiers": "In derselben RadarPro-App enthält die kostenlose Version die Karte, die Radar-Punkte, Vordergrundwarnungen und manuelle Datenaktualisierungen. Pro ergänzt Hintergrundwarnungen, automatische Aktualisierungen und Fahrterkennung – jeweils mit den nötigen Berechtigungen.",
        "sections": [
            (
                "warnungen",
                "Wie funktionieren Radarwarnungen?",
                "RadarPro vergleicht deine Position mit den Radar- und Kontrollpunkten seiner Datenbank und nennt beim Annähern per Sprache die Entfernung und, wenn verfügbar, das Tempolimit. Karte, Vordergrundwarnungen und manuelle Aktualisierungen bleiben in der kostenlosen Version verfügbar. Warnabstand und Abdeckung hängen von der Art des Punktes, den verfügbaren Daten und der Genauigkeit der Ortung ab.",
            ),
            (
                "behoerde",
                "Ist RadarPro ein offizieller Dienst einer Behörde?",
                "Nein. RadarPro ist unabhängig und keine offizielle Anwendung einer Verkehrsbehörde; es besteht keine Verbindung zu einer Behörde. Veröffentlichte Informationen deiner Behörde und die Beschilderung vor Ort haben immer Vorrang.",
            ),
            (
                "eds-abschnitt",
                "Was ist der Unterschied zwischen EDS und einer Abschnittskontrolle?",
                "EDS ist in der Türkei die Bezeichnung für elektronische Verkehrskontrollsysteme. Bei einer Abschnittskontrolle wird die Geschwindigkeit über Strecke und Zeit zwischen Einfahrt und Ausfahrt gemessen. RadarPro bietet für unterstützte Abschnitte Hinweise zu Einfahrt, Durchschnittsgeschwindigkeit im Abschnitt und Ausfahrt. Das zulässige Tempo ergeben Beschilderung und Verkehrsregeln.",
            ),
            (
                "hintergrund",
                "Funktionieren Warnungen, während eine andere Navigations-App läuft?",
                "Pro enthält Sprachwarnungen im Hintergrund, sofern die nötigen Standort- und Audiorechte erteilt sind. In der kostenlosen Version laufen Warnungen, solange RadarPro im Vordergrund ist. Berechtigte neue Nutzer können Hintergrundwarnungen zusätzlich in einer einmaligen Einführung erleben. Betriebssystem, Energiesparen, Audioausgabe und Berechtigungen können Warnungen beeinflussen.",
            ),
            (
                "daten",
                "Wie werden neue Blitzer und Datenaktualisierungen behandelt?",
                "RadarPro nutzt seine vorhandene Datenbank; ein neu installierter, versetzter oder entfernter Blitzer kann noch fehlen. Kostenlose Nutzer können manuell aktualisieren. Pro enthält automatische Aktualisierungen, wenn Verbindung und eine veröffentlichte Aktualisierung vorliegen. Die Karte ist keine vollständige oder immer aktuelle Liste aller Blitzer weltweit.",
            ),
            (
                "einfuehrung-testphase",
                "Ist die Einführung dasselbe wie die Testphase des Pro-Abos?",
                "Nein. In der einmaligen Einführung eines berechtigten neuen Nutzers sind drei verschiedene, tatsächlich zu Ende gesprochene Hintergrund-Ansagen zu Radar/EDS die Bewertungsschwelle; diese Einführung startet kein Abo. Die 14-tägige Testphase im Store ist davon getrennt und kann bei einem berechtigten Jahresangebot von Pro verfügbar sein. Berechtigung, Verlängerung und Preis stehen auf dem Kaufbildschirm.",
            ),
            (
                "sicherheit",
                "Bedeutet RadarPro, dass ich kein Bußgeld bekomme?",
                "Nein. RadarPro ist eine Hilfe für mehr Aufmerksamkeit beim Fahren. Halte Tempolimits und örtliche Regeln ein und schaue während der Fahrt nicht auf den Bildschirm oder in einen Kaufvorgang. Daten, Ortung und Gerätezustand machen eine Warnung vor jedem Blitzer in jeder Situation unmöglich.",
            ),
        ],
        "download_h2": "RadarPro für iOS oder Android",
        "download_p": "Starte mit der kostenlosen Karte und Vordergrundwarnungen. Pro-Angebote, lokale Preise und etwaige Testbedingungen findest du auf dem Kaufbildschirm in der App.",
        "store_primary": "Im App Store laden",
        "store_secondary": "Bei Google Play",
        "footer_experience": "Fahrerlebnis",
        "footer_privacy": "Datenschutz (Englisch)",
        "footer_terms": "Nutzungsbedingungen (Englisch)",
    },
    "ru": {
        "lang_attr": "ru",
        "dir": "ltr",
        "file": "guide-ru.html",
        "title": "Гид: радары, камеры и участки средней скорости | RadarPro",
        "desc": "Что сообщает RadarPro, как работают стационарные камеры, камеры на красный свет и участки средней скорости, и где заканчиваются данные.",
        "skip": "Перейти к содержанию",
        "contents_label": "Гид по радарам и скорости",
        "h1": "Радары, камеры и участки средней скорости",
        "intro": "Перед поездкой полезно понимать, что именно сообщает предупреждение и где заканчиваются данные. RadarPro — независимое приложение-помощник с голосовыми предупреждениями о точках из своей базы.",
        "tiers": "В том же приложении RadarPro бесплатная версия включает карту, точки радаров, предупреждения на экране и ручное обновление данных. Pro добавляет фоновые предупреждения, автоматические обновления и определение поездки — при наличии нужных разрешений.",
        "sections": [
            (
                "warnings",
                "Как работают предупреждения о радарах?",
                "RadarPro сравнивает ваше местоположение с точками радаров и контроля из своей базы и при приближении голосом сообщает расстояние и, когда есть данные, ограничение скорости. Карта, предупреждения на экране и ручное обновление остаются в бесплатной версии. Дистанция предупреждения и покрытие зависят от типа точки, доступных данных и точности определения местоположения.",
            ),
            (
                "official",
                "RadarPro — официальный сервис ведомства?",
                "Нет. RadarPro независим и не является официальным приложением органов регулирования дорожного движения, связи с ними нет. Опубликованная информация вашего ведомства и знаки на дороге всегда важнее.",
            ),
            (
                "eds-average",
                "Чем EDS отличается от участка средней скорости?",
                "EDS — принятое в Турции название электронных систем контроля дорожного движения. На участке средней скорости скорость оценивают по расстоянию и времени между въездом и выездом. RadarPro подсказывает о въезде, средней скорости внутри участка и выезде там, где участок поддерживается. Допустимую скорость определяют знаки и правила движения.",
            ),
            (
                "background",
                "Работают ли предупреждения при открытом навигаторе?",
                "Pro включает голосовые фоновые предупреждения при наличии разрешений на геолокацию и звук. В бесплатной версии предупреждения работают, когда RadarPro открыт на экране. Подходящие новые пользователи также могут испытать фоновые предупреждения в разовом вводном режиме. Операционная система, энергосбережение, аудиовыход и разрешения могут влиять на предупреждения.",
            ),
            (
                "data",
                "Как учитываются новые камеры и обновления данных?",
                "RadarPro использует свою базу; только что установленная, перенесённая или снятая камера может в ней ещё отсутствовать. В бесплатной версии обновление выполняется вручную. Pro обновляет данные автоматически, когда есть связь и опубликовано обновление. Карта не является полным и всегда актуальным списком всех камер мира.",
            ),
            (
                "intro-trial",
                "Вводный режим — это то же, что пробный период подписки Pro?",
                "Нет. В разовом вводном режиме для подходящего нового пользователя порогом оценки служат три разных фоновых сообщения о радаре или EDS, которые действительно были произнесены до конца; подписка при этом не начинается. Отдельный 14-дневный пробный период в магазине может предлагаться при подходящем годовом предложении Pro. Условия, продление и цену смотрите на экране покупки.",
            ),
            (
                "safety",
                "Значит ли RadarPro, что штрафа не будет?",
                "Нет. RadarPro — помощник для внимательности за рулём. Соблюдайте ограничения скорости и местные правила и не смотрите на экран или на процесс покупки во время движения. Из-за данных, геолокации и состояния устройства гарантировать предупреждение о каждой камере в любой ситуации невозможно.",
            ),
        ],
        "download_h2": "RadarPro для iOS и Android",
        "download_p": "Начните с бесплатной карты и предупреждений на экране. Предложения Pro, местные цены и условия пробного периода — на экране покупки в приложении.",
        "store_primary": "Загрузить в App Store",
        "store_secondary": "Доступно в Google Play",
        "footer_experience": "Режим поездки",
        "footer_privacy": "Политика конфиденциальности (англ.)",
        "footer_terms": "Условия использования (англ.)",
    },
    "ar": {
        "lang_attr": "ar",
        "dir": "rtl",
        "file": "guide-ar.html",
        "title": "دليل الرادارات وكاميرات السرعة ومقاطع السرعة المتوسطة | RadarPro",
        "desc": "ماذا ينبّهك RadarPro، وكيف تعمل الرادارات الثابتة وكاميرات الإشارة الحمراء ومقاطع السرعة المتوسطة، وأين تنتهي البيانات.",
        "skip": "انتقل إلى المحتوى",
        "contents_label": "دليل الرادارات والسرعة",
        "h1": "الرادارات وكاميرات السرعة ومقاطع السرعة المتوسطة",
        "intro": "قبل الانطلاق، من المفيد معرفة ما يقوله التنبيه وأين تنتهي بياناته. RadarPro تطبيق مستقل للتوعية أثناء القيادة، مع تنبيهات صوتية للنقاط في قاعدته.",
        "tiers": "داخل التطبيق نفسه، تشمل النسخة المجانية الخريطة ونقاط الرادارات والتنبيهات أثناء فتح التطبيق والتحديثات اليدوية للبيانات. ويضيف Pro تنبيهات في الخلفية وتحديثات تلقائية واكتشاف القيادة مع الأذونات اللازمة.",
        "sections": [
            (
                "alerts",
                "كيف تعمل تنبيهات الرادارات؟",
                "يقارن RadarPro موقعك بنقاط الرادارات والتحكم في قاعدته، وعند الاقتراب يُعلن صوتيًا المسافة، وحد السرعة عند توفره. تبقى الخريطة والتنبيهات أثناء فتح التطبيق والتحديثات اليدوية متاحة في النسخة المجانية. تعتمد مسافة التنبيه والتغطية على نوع النقطة والبيانات المتاحة ودقة تحديد الموقع.",
            ),
            (
                "official",
                "هل RadarPro خدمة رسمية لجهة مرورية؟",
                "لا. RadarPro مستقل وليس تطبيقًا رسميًا لأي جهة مرورية، ولا توجد أي صلة بينه وبينها. المعلومات المنشورة من جهة بلدك واللوحات على الطريق لها الأولوية دائمًا.",
            ),
            (
                "eds-average",
                "ما الفرق بين EDS ومقطع السرعة المتوسطة؟",
                "EDS هو الاسم المستخدم في تركيا لأنظمة التحكم الإلكتروني في المرور. وفي مقطع السرعة المتوسطة تُقاس السرعة اعتمادًا على المسافة والزمن بين الدخول والخروج. يوفّر RadarPro تنبيهات الدخول ومتوسط السرعة داخل المقطع والخروج في المقاطع المدعومة. وتحدّد اللوحات وقواعد المرور السرعة المطبقة.",
            ),
            (
                "background",
                "هل تعمل التنبيهات مع تشغيل تطبيق ملاحة آخر؟",
                "يشمل Pro تنبيهات صوتية في الخلفية مع أذونات الموقع والصوت اللازمة. وفي النسخة المجانية تعمل التنبيهات وRadarPro مفتوح. ويمكن للمستخدمين الجدد المؤهلين تجربة التنبيهات في الخلفية أيضًا خلال تجربة تعريفية لمرة واحدة. وقد يؤثر نظام التشغيل وتوفير الطاقة ومخرج الصوت والأذونات في التنبيهات.",
            ),
            (
                "data",
                "كيف تُعالج الكاميرات الجديدة وتحديثات البيانات؟",
                "يستخدم RadarPro قاعدته الحالية؛ وقد لا تظهر كاميرا مثبتة أو منقولة أو مزالة حديثًا. يمكن للمستخدمين المجانيين التحديث يدويًا. ويشمل Pro تحديثات تلقائية عند توفر الاتصال وتحديث منشور. والخريطة ليست قائمة كاملة أو محدثة دائمًا لكل الكاميرات في العالم.",
            ),
            (
                "intro-trial",
                "هل التجربة التعريفية هي نفسها فترة تجربة اشتراك Pro؟",
                "لا. في التجربة التعريفية لمرة واحدة لمستخدم جديد مؤهل، يكون حد التقييم ثلاثة إعلانات مختلفة في الخلفية عن رادار أو EDS تُنطق حتى النهاية فعلًا؛ وهذه التجربة لا تبدأ أي اشتراك. أما فترة التجربة في المتجر ومدتها 14 يومًا فهي منفصلة وقد تُتاح مع عرض سنوي مؤهل من Pro. راجع الأهلية والتجديد والسعر في شاشة الشراء.",
            ),
            (
                "safety",
                "هل يعني استخدام RadarPro أنني لن أُغرَّم؟",
                "لا. RadarPro مساعد للتوعية أثناء القيادة. التزم بحدود السرعة والقواعد المحلية، ولا تنظر إلى الشاشة أو إلى عملية شراء أثناء القيادة. وبسبب البيانات والموقع وحالة الجهاز لا يمكن ضمان تنبيه لكل كاميرا في كل حالة.",
            ),
        ],
        "download_h2": "استخدم RadarPro على iOS أو Android",
        "download_p": "ابدأ بالخريطة المجانية والتنبيهات أثناء فتح التطبيق. راجع عروض Pro والأسعار المحلية وأي شروط تجربة في شاشة الشراء داخل التطبيق.",
        "store_primary": "تنزيل من App Store",
        "store_secondary": "متوفر على Google Play",
        "footer_experience": "تجربة القيادة",
        "footer_privacy": "سياسة الخصوصية (بالإنجليزية)",
        "footer_terms": "شروط الاستخدام (بالإنجليزية)",
    },
    "pt": {
        "lang_attr": "pt-BR",
        "dir": "ltr",
        "file": "guide-pt.html",
        "title": "Guia de radares, pardais e trechos de velocidade média | RadarPro",
        "desc": "O que o RadarPro avisa, como funcionam radares fixos, pardais, câmeras de semáforo e trechos de velocidade média, e onde os dados terminam.",
        "skip": "Ir para o conteúdo",
        "contents_label": "Guia de radares e velocidade",
        "h1": "Radares, pardais e trechos de velocidade média",
        "intro": "Antes de pegar a estrada, vale entender o que um aviso informa e onde o dado termina. O RadarPro é um app independente de atenção à direção, com avisos falados para os pontos da sua base.",
        "tiers": "No mesmo app RadarPro, a versão gratuita inclui o mapa, os pontos de radares, os avisos em primeiro plano e as atualizações manuais de dados. O Pro adiciona avisos em segundo plano, atualizações automáticas e detecção de direção com as permissões necessárias.",
        "sections": [
            (
                "avisos",
                "Como funcionam os avisos de radares?",
                "O RadarPro compara sua posição com os pontos de radar e de fiscalização da sua base e, na aproximação, fala a distância e, quando existe, o limite de velocidade. O mapa, os avisos em primeiro plano e as atualizações manuais continuam na versão gratuita. A distância do aviso e a cobertura dependem do tipo de ponto, dos dados disponíveis e da precisão da localização.",
            ),
            (
                "oficial",
                "O RadarPro é um serviço oficial de trânsito?",
                "Não. O RadarPro é independente, não é um aplicativo oficial de nenhum órgão de trânsito e não tem vínculo com eles. As informações publicadas pelo órgão do seu país e a sinalização na via têm prioridade sempre.",
            ),
            (
                "eds-trecho",
                "Qual é a diferença entre EDS e um trecho de velocidade média?",
                "EDS é o nome usado na Turquia para os sistemas eletrônicos de fiscalização de trânsito. Em um trecho de velocidade média, a velocidade é calculada pela distância e pelo tempo entre a entrada e a saída. O RadarPro avisa sobre entrada, velocidade média dentro do trecho e saída nos trechos compatíveis. O limite aplicável é definido pela sinalização e pelas regras de trânsito.",
            ),
            (
                "segundo-plano",
                "Os avisos funcionam com outro app de navegação aberto?",
                "O Pro inclui avisos falados em segundo plano com as permissões de localização e áudio necessárias. Na versão gratuita, os avisos funcionam com o RadarPro aberto. Usuários novos elegíveis também podem experimentar os avisos em segundo plano em uma experiência inicial única. Sistema operacional, economia de energia, saída de áudio e permissões podem afetar os avisos.",
            ),
            (
                "dados",
                "Como são tratados radares novos e atualizações de dados?",
                "O RadarPro usa a base que já tem; um radar recém-instalado, movido ou removido pode ainda não aparecer. Usuários gratuitos podem atualizar manualmente. O Pro inclui atualizações automáticas quando há conexão e uma atualização publicada. O mapa não é uma lista completa nem sempre atualizada de todos os radares do mundo.",
            ),
            (
                "inicio-teste",
                "A experiência inicial é o mesmo que o teste da assinatura Pro?",
                "Não. Na experiência inicial única de um usuário novo elegível, o critério de avaliação são três anúncios diferentes de radar/EDS em segundo plano que realmente terminem de ser falados; essa experiência não inicia assinatura. O teste de 14 dias na loja é separado e pode existir em uma oferta anual elegível do Pro. Veja elegibilidade, renovação e preço na tela de compra.",
            ),
            (
                "seguranca",
                "Usar o RadarPro significa que não serei multado?",
                "Não. O RadarPro é uma ajuda para a atenção ao dirigir. Respeite os limites de velocidade e as regras locais e não olhe para a tela nem para um fluxo de compra enquanto dirige. Dados, localização e condições do aparelho impedem garantir aviso de todo radar em qualquer situação.",
            ),
        ],
        "download_h2": "Use o RadarPro no iOS ou Android",
        "download_p": "Comece com o mapa gratuito e os avisos em primeiro plano. Veja as ofertas Pro, os preços locais e as condições de teste na tela de compra dentro do app.",
        "store_primary": "Baixar na App Store",
        "store_secondary": "Disponível no Google Play",
        "footer_experience": "Experiência de direção",
        "footer_privacy": "Política de privacidade (inglês)",
        "footer_terms": "Termos de uso (inglês)",
    },
}


def hreflang_block(current: str) -> str:
    lines = []
    for lang, filename in GUIDES.items():
        lines.append(
            f'    <link rel="alternate" hreflang="{lang}" href="{SITE}/{filename}" />'
        )
    lines.append(
        f'    <link rel="alternate" hreflang="x-default" href="{SITE}/{GUIDES["tr"]}" />'
    )
    return "\n".join(lines)


def nav(current: str) -> str:
    parts = []
    for lang, filename in GUIDES.items():
        label, title = NAV_LABEL[lang], NAV_TITLE[lang]
        current_attr = (
            ' aria-current="page"' if lang == current else ""
        )
        parts.append(
            f'<a href="./{filename}" hreflang="{lang}" lang="{lang}" '
            f'title="{title}" aria-label="{title}"{current_attr}>{label}</a>'
        )
    return "".join(parts)


def build(locale: str, c: dict) -> str:
    anchor_ids = [s[0] for s in c["sections"]]
    toc = "".join(
        f'<li><a href="#{sid}">{title}</a></li>' for sid, title, _ in c["sections"]
    )
    body = "".join(
        f'<section id="{sid}"><h2>{title}</h2><p>{text}</p></section>'
        for sid, title, text in c["sections"]
    )
    faq = {
        "@type": "FAQPage",
        "@id": f"{SITE}/{c['file']}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": title,
                "acceptedAnswer": {"@type": "Answer", "text": text},
            }
            for _, title, text in c["sections"]
        ],
    }
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "url": f"{SITE}/",
                "name": "RadarPro",
                "inLanguage": list(GUIDES.keys()),
            },
            {
                "@type": "WebPage",
                "@id": f"{SITE}/{c['file']}#webpage",
                "url": f"{SITE}/{c['file']}",
                "name": c["title"],
                "description": c["desc"],
                "inLanguage": c["lang_attr"],
                "isPartOf": {"@id": f"{SITE}/#website"},
            },
            faq,
        ],
    }
    ld = json.dumps(graph, ensure_ascii=False, indent=2)

    return f"""<!doctype html>
<html lang="{c['lang_attr']}" dir="{c['dir']}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#050507">
<title>{c['title']}</title>
<meta name="description" content="{c['desc']}" />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="{SITE}/{c['file']}" />
{hreflang_block(locale)}
<meta property="og:type" content="article" />
<meta property="og:site_name" content="RadarPro" />
<meta property="og:url" content="{SITE}/{c['file']}" />
<meta property="og:title" content="{c['title']}" />
<meta property="og:description" content="{c['desc']}" />
<meta property="og:image" content="{SITE}/assets/brand/radarpro-icon.png" />
<meta name="twitter:card" content="summary" />
<meta name="twitter:title" content="{c['title']}" />
<meta name="twitter:description" content="{c['desc']}" />
<meta name="twitter:image" content="{SITE}/assets/brand/radarpro-icon.png" />
<script type="application/ld+json">{ld}</script>
<link rel="icon" href="./assets/brand/radarpro-icon.png">
<link rel="stylesheet" href="./legal.css"><link rel="stylesheet" href="./guide.css">
</head><body>
<a class="skip" href="#content">{c['skip']}</a>
<header><a class="brand" href="./"><img src="./assets/brand/radarpro-icon.png" width="32" height="32" alt="">RADAR<span>PRO</span></a><nav aria-label="Language">{nav(locale)}</nav></header>
<main id="content"><p class="eyebrow">RadarPro</p><h1>{c['h1']}</h1><p class="rp-guide-intro">{c['intro']}</p><p>{c['tiers']}</p>
<nav class="contents" aria-label="{c['contents_label']}"><ol>{toc}</ol></nav>
{body}
<section id="download"><h2>{c['download_h2']}</h2><p>{c['download_p']}</p><div class="rp-boot-actions">
      <a class="rp-boot-primary" href="{APP_STORE}">{c['store_primary']}</a>
      <a class="rp-boot-secondary" href="{PLAY_STORE}">{c['store_secondary']}</a>
    </div></section>
</main><footer><a href="./{locale}.html">{c['footer_experience']}</a><a href="./privacy.html" hreflang="en" lang="en">{c['footer_privacy']}</a><a href="./terms.html" hreflang="en" lang="en">{c['footer_terms']}</a><a href="mailto:support@radarpro.online">support@radarpro.online</a><p>© 2026 RadarPro</p></footer>
</body></html>
"""


def main() -> None:
    for locale, content in CONTENT.items():
        path = ROOT / content["file"]
        io.open(path, "w", encoding="utf-8").write(build(locale, content))
        print(f"{path.name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
