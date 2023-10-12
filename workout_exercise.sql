(1,'wznosy jednoracz w bok','jedna ręka trzyma bramkę, ciało pochylone w bok, nogi złaczone, wznosy reki na wysokosc oczu, łokieć lekko ugięty','barki'),
(2,'wyciskanie siedzac na ławce','plecy oparte o ławkę, opuszczanie hantli głęboko','barki'),
(3,'wycskanie francuskie leżac podchwytem','u góry moment zatrzymania','triceps'),
(4,'wznosy do przodu w pochyleniu','na ławce opierając się przodem wznosy wyprostowanych rąk przed siebie, zatrzymanie u góry','barki'),
(5,'wyprosty rąk z uchwytem warkoczowym na bramie','rozszerzanie u dołu, pełen wyprost i zatrzymanie','triceps'),
(6,'wiosłowanie siedząc','maszyna przy bieżniach, łokcie wysoko','plecy'),
(7,'ściąganie drążka od góry za kark','drugi uchwyt od góry ze stojaka','plecy'),
(8,'wiosłowanie sztangielki jednorącz w opadzie','zwiększać ciężar','plecy'),
(9,'uginanie ręki ze sztangielką na modlitewniku','pełen wyprost, moment zatrzynamnia u góry i u dołu, u góry sztangielka jakby za uchem','biceps'),
(10,'uginanie oburącz stojąc sztanga łamana','do pełnego wyprostu, wolno, trzymając szeroko','biceps'),
(11,'przysiady ze sztangą','zwiększać ciężar','nogi'),
(12,'wypychanie jednonóż  na maszynie','moment zatrzymania/spięcia przy wypchnięciu','nogi'),
(13,'przywodziciele na paszynie','zatrzymanie przy złączeniu, stopy prostopadłe','nogi'),
(14,'wykroki','od szyby do lodówki i spowrotem','nogi'),
(15,'wyprosty na maszynie','moment zatrzymania u góry','nogi'),
(16,'zginanie na maszynie w pozycji siedzącej','obunóż ','nogi'),
(17,'wspiętki na palcach stojąc','na łydki','nogi'),
(18,'wyciskanie na bramce z wygiętą sztangą','skos dodatni - 3 ząbek w ławce i z przpdu podniesione na max siedzenie','klatka'),
(19,'rozpiętki na skosie dodatnim','nowa ławka, łokcie lekko zgięte, maksymalnie do dołu','klatka'),
(20,'wyciskanie sztangi na płasko','z małym obciążeniem ale wiele razy, ręce szeroko, opuszczać do mostka','klatka'),
(21,'w zwisie podciąganie nóg do klatki','nie opuszczać za nisko, cały czas napięcie brzucha','brzuch'),
++(22,'kołyska','maszyna w drugiej sali','brzuch'),
(34,'wznosy na maszynie w sali do nóg','belka na wysokości ramion, twarzą do lustra','barki'),
(35,'wypypachnieod klatki do góry','wyciąg od dołu, uchwyt z rączkami zakręconymi do góry','barki'),
(36,'wyprosty rąk przed siebie z gumą stojąc','lekko się pochylić, ręce wysoko przed siebie i chwila zatrzymania','barki'),
(37,'podsiąganie uchwytu na brame do brody','uchwyt prosty, mocowany od dołu','barki'),
(38,'trójką uchwyt od dołu','na bramie, kaptury','barki'),
(39,'protowanie rąk na bramie uchwytem prostym','podchwytem, uchwyt prosty, zatrzymanie u dołu i u góry ','triceps'),
(40,'wyciskanie wąskie sztangi leżąc','łokcie na zewnątrz','triceps'),
(45,'wiosłowanie sztangą poprzeczną wąski','sztanga przy drzwiach','plecy'),
(46,'ściąganie z góry do klatki kółkowy uchwyt','uchwyt kółkowy','plecy'),
(47,'wiosłowanie siedząc, uchwyt 5 od góry','maszyna przy szklanych drzwiach','plecy'),
(48,'uginanie sztangi łamanej w podprze brzucha','skos dodatni, w oparciu o ławkę uginanie rąk ze sztangą za ławką ','biceps'),
(49,'uginanie rąk ze sztangą  stojąc','bezpośrednio przy ścianie','biceps'),
(57,'prostowanie nóg na suwnicy siedzącej','progres','nogi'),
(58,'przysiady z zahaczonymi nogami','jak najbardziej do tyłu i pełny przysiad','nogi'),
(59,'uginanie obunóż na maszynie leżąc',NULL,'nogi'),
(60,'w siedzeniu proste nogi uniesione oddalanie','z obciążnikami, lekko wyhylenie do tyłu, nogi proste do góry i przygliżanie piętami do środka i odwodzenie, stopy prostopadłe','nogi'),
(61,'oparcie na psa u8gięta noga w bok','w oparciu dłońmi, kolana zgięte noga z obciążeniem zgięta do góry w bok','nogi'),
(62,'w oparciu na łokciach prosta wnoga do góry','z obciążeniem, noga wyprostowana, stopa prostopadle','nogi'),
(63,'w oparciu na łokciach zgięta noga do góry','z obciążeniem zgięta noga do góry w płaszczyznie pionowej','nogi'),
(64,'łydki siedząc','siedząc na maszynie','nogi'),
(65,'maszyna-motylek','łokcie zgięte, wysoko, barki niżej, głęboko do tyłu','klatka'),
(66,'wypychanie przed siebie siedząc, maszyna','maszyna przy ścianie i bieżniach','klatka'),
(67,'przenoszenie hantla poprzek ławki','wydech przy opuszczeniu, gdy do góry to wdech','klatka'),
(68,'allachy','wydech przy zgięciu','brzuch')





select plan.data_from, plan.data_to, plan.day, exercise.name, exercise.description, exercise.body_part, series.number_sets, series.number_repeats, series.weight, series.superseries, series.set, plan.order from exercise inner join series on exercise.ide = series.id_exercise inner join plan on series.ids = plan.id_series and plan.data_from = '2023-06-20' and plan.day=1  order by plan.order
jest plan

select plan.data_from, plan.data_to, plan.day, exercise.name, exercise.description, exercise.body_part, series.number_sets, series.number_repeats, series.weight, series.superseries, series.set, plan.order from exercise inner join series on exercise.ide = series.id_exercise inner join plan on series.ids = plan.id_series and plan.data_from = '2023-05-20' and plan.day=1  order by plan.order

jest pusto


