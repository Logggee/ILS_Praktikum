# Ausarbeitung Versuch 1 ILS
## Aufgabe 1
### a

## Aufgabe 2
### a
Der Abstrakte Konstrukter der Klasse Classifier, übergibt den Paramter C an sein Attribut C. C legt die anzahl an möglichen Klassen fest, in die die Daten unterteilt werden können.

Die Methode fit wird für das Trainieren des Klassifikators benutzt. Die Methode bekommt die Parameter X und T, wobei X die Daten und T die dazugehörigen Klassenlabel sind.

Die Methode predict Klassifiziert anhand des Trainings neu übergabene Daten ein. Als Parameter übergibt man Predict z.B. einen neuen Vektor um ihn Klassifizieren zu lasse.

Die Methode Crossvalidate teilt die Daten in S Teile auf. Der Parameter X ist für die Übergabe der Daten zuständig und der Parameter S gibt an, in wie viele Blöcke die Daten X geteilt werden sollen. Der dritte Parameter T sind die Klassenlabel für die Daten in X. Die Methode Crossvalidate macht eine Kreuzvalidierung mit dem Entsprachenden Modell in dem sie implementiert wird. Dies bedeutet, dass die Daten in X in S Blöcke geteilt werden und ein Block nicht zum Trainieren verwendet wird, sondern zum Validieren. Die Kreuzvalidierung macht jedoch mit jedem Block aus X eine Validierung und mittelt daraus dann die Genauigkeit.

### b
* Das Array in idxS enthält die Einträge bei den Parametern N=9 und S=3 [range(0, 3), range(3, 6), range(6, 9)]. Das Array aus 9 Daten soll in 3 gleich große Teile aufgeteilt werden. somit kommen dann die drei ranges zu stande.
* idxVal enthält für jeden Schleifendurchgang einen der range Einträge aus der Liste idxS. idxTrain enthält die restlichen Blöcke die nicht in der Range von idxVal liegen.
* In perm ist eine zufällige Reihenfolge aus Indexen für X. Dies ist sinnvoll, da wir die Daten in X nicht in der vorgegeben Reihenfolge verarbeiten wollen, da diese schon eine Art Ordung haben könnten. Somit indizieren wir mit einer Range aus den perm Indexen auf die Daten X und die Label T mit denen wir dann das Modell trainieren wollen.
* 1 Durchlauf: x[3], x[1], x[0]
2 Durchlauf: x[8], x[2], x[4]
3 Durchlauf: x[7], x[5], x[6]
* Der Returnwert err ist der prediction error, die Formel dafür befindet sich auf Seite 115 Nummer 2.108 (FP + FN) / (TP + FP + FN + TN). Der Returnwert MatCp ist die Confusion Matrix welche die Werte False Positive (FP), False Negative (FN), True Positive (TP) und True Negative (TN) enthält.