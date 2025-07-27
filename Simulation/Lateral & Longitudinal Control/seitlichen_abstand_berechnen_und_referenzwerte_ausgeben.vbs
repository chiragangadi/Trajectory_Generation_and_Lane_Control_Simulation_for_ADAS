' In den folgenden Zeilen werden die Namen
' der Ausgaenge festgelegt
' Output(1) = "Seitlicher_Abstand_ltr"
' Output(2) = "Position_S"
' Output(3) = "V_ref"
' Output(4) = "V_max"
' Output(5) = "Simulation_beenden"

' Die folgenden Variablen sind globale Variablen und 
' stehen waehrend der gesamten Simulation zur Verfuegung
dim X_strecke()
dim Y_strecke()
dim S_strecke()
dim Vmax_strecke()
dim Vref_strecke()
dim daten_eingelesen
dim i_kleiner_alt
dim sp_kleiner_alt

function main(Init, psi, pos_x, pos_y)
    
    ' Anzahl der Ausgaenge
    dim Output(5)
    
    ' Variablen fuer die Dateioperationen
    dim count, fso_x, fso_y
    dim fso_s, fso_vmax, fso_vref
    dim org_zeile_X, org_zeile_Y
    dim org_zeile_S, org_zeile_Vmax, org_zeile_Vref
    dim dateiPfad_X, dateiPfad_Y
    dim dateiPfad_S, dateiPfad_Vmax, dateiPfad_Vref
    dim x_eingelesen, y_eingelesen
    dim s_eingelesen, vmax_eingelesen, vref_eingelesen
    
    ' Variablen fuer die Berechnungen
    dim p_x, p_y
    dim q_x, q_y
    dim i, i_kleiner
    dim bedingung
    dim dx1, dy1, dx2, dy2, l1, l2
    dim nx1, ny1, nx2, ny2
    dim rho1, rho2
    dim det_1, det_2, det_3, det_4
    dim e_x, e_y
    dim seitlicher_abstand
    
    ' Variablen fuer die Position, Geschwindigkeitssollwerte und Maximalgeschwindigkeit
    dim sp, sp_kleiner
    dim pos_S, pos_V_ref, pos_V_max
    dim m_V_ref_N, m_V_max_N, m_V_max_ref_Z, m_V_ref, m_V_max
    
    ' Die Konstante pi muss man selbst definieren
    const pi = 3.1415926535
    
    ' Da die Variablen in VBS nicht typisiert sind, kann es bei
    ' der Verwendung von '+' fuer die Addition zu Fehlern kommen.
    ' Deshalb muss eine Addition in VBS ist durch -- realisiert werden.
    
    i = 0
    
    ' Waehrend der Initialisierung der Simulation ist Init = 1
    if (Init = 1) then
        
        const ForReading = 1
        
        ' Einzulesende Dateien mit vollstaendigem Pfad
        dateiPfad_X    = "C:\FAS\Laengs-_und_Querregelung\Strecke_rechts_X.txt"
        dateiPfad_Y    = "C:\FAS\Laengs-_und_Querregelung\Strecke_rechts_Y.txt"
        dateiPfad_S    = "C:\FAS\Laengs-_und_Querregelung\V-Profil_pos.txt"
        dateiPfad_Vmax = "C:\FAS\Laengs-_und_Querregelung\V-Profil_max.txt"
        dateiPfad_Vref = "C:\FAS\Laengs-_und_Querregelung\V-Profil_ref.txt"
        
        ' Variablen initialisieren
        x_eingelesen = 0
        y_eingelesen = 0
        s_eingelesen = 0
        vmax_eingelesen = 0
        vref_eingelesen = 0
        daten_eingelesen = 0
        i_kleiner = 1
        i_kleiner_alt = 1
        sp_kleiner = 1
        sp_kleiner_alt = 1
        
        ' Datei mit den x-Koordinaten einlesen
        ' FileSystemObject fuer die erste einzulesende Datei anlegen
        set fso_x = CreateObject("Scripting.FileSystemObject")
        ' Pruefen, ob die Datei vorhanden ist...
        if (fso_x.FileExists(dateiPfad_X)) then
            ' Oeffnen der Datei zum Lesen der x-Werte
            set file_x = fso_x.OpenTextFile(dateiPfad_X, ForReading)
            ' Indexzaehler auf 0 setzen
            count = 0
            ' Solange einlesen, bis das Ende der Datei erreicht ist
            do while (file_x.AtendOfStream <> true)
                count = count -- 1
                ' Array vergroessern, damit wir beim Einlesen flexibel sind
                redim preserve X_strecke(count)
                ' Zeilenweise Einlesen der Textdatei
                org_zeile_X = file_x.Readline
                ' Ausgelesene Zeile in Array zwischenspeichern
                X_strecke(count) = CDbl(org_zeile_X)
            loop
            ' Datei schliessen...
            file_x.Close
            ' Flag "x-Daten wurden eingelesen" setzen
            x_eingelesen = 1
        end if
        
        
        ' Datei mit den y-Koordinaten einlesen
        ' FileSystemObject fuer die zweite einzulesende Datei anlegen
        set fso_y = CreateObject("Scripting.FileSystemObject")
        ' Pruefen, ob die Datei vorhanden ist...
        if (fso_y.FileExists(dateiPfad_Y)) then
            ' Oeffnen der Datei zum Lesen der y-Werte
            set file_y = fso_y.OpenTextFile(dateiPfad_Y, ForReading)
            ' Indexzaehler auf 0 setzen
            count = 0
            ' Solange einlesen, bis das Ende der Datei erreicht ist
            do while (file_y.AtendOfStream <> true)
                count = count -- 1
                ' Array vergroessern, damit wir beim Einlesen flexibel sind
                redim preserve Y_strecke(count)
                ' Zeilenweise Einlesen der Textdatei
                org_zeile_Y = file_y.Readline
                ' Ausgelesene Zeile in Array zwischenspeichern
                Y_strecke(count) = CDbl(org_zeile_Y)
            loop
            ' Datei schliessen...
            file_y.Close
            ' Flag "y-Daten wurden eingelesen" setzen
            y_eingelesen = 1
        end if
        
        
        ' Datei mit den Positionswerten S einlesen
        ' FileSystemObject fuer die dritte einzulesende Datei anlegen
        set fso_s = CreateObject("Scripting.FileSystemObject")
        ' Pruefen, ob die Datei vorhanden ist...
        if (fso_s.FileExists(dateiPfad_S)) then
            ' Oeffnen der Datei zum Lesen der S-Werte
            set file_s = fso_s.OpenTextFile(dateiPfad_S, ForReading)
            ' Indexzaehler auf 0 setzen
            count = 0
            ' Solange einlesen, bis das Ende der Datei erreicht ist
            do while (file_s.AtendOfStream <> true)
                count = count -- 1
                ' Array vergroessern, damit wir beim Einlesen flexibel sind
                redim preserve S_strecke(count)
                ' Zeilenweise Einlesen der Textdatei
                org_zeile_S = file_s.Readline
                ' Ausgelesene Zeile in Array zwischenspeichern
                S_strecke(count) = CDbl(org_zeile_S)
            loop
            ' Datei schliessen...
            file_s.Close
            ' Flag "s-Daten wurden eingelesen" setzen
            s_eingelesen = 1
        end if
        
        
        ' Datei mit dem vorberechneten Maximalwertprofil einlesen
        ' FileSystemObject fuer die vierte einzulesende Datei anlegen
        set fso_vmax = CreateObject("Scripting.FileSystemObject")
        ' Pruefen, ob die Datei vorhanden ist...
        if (fso_vmax.FileExists(dateiPfad_Vmax)) then
            ' Oeffnen der Datei zum Lesen der Vmax-Werte
            set file_vmax = fso_vmax.OpenTextFile(dateiPfad_Vmax, ForReading)
            ' Indexzaehler auf 0 setzen
            count = 0
            ' Solange einlesen, bis das Ende der Datei erreicht ist
            do while (file_vmax.AtendOfStream <> true)
                count = count -- 1
                ' Array vergroessern, damit wir beim Einlesen flexibel sind
                redim preserve Vmax_strecke(count)
                ' Zeilenweise Einlesen der Textdatei
                org_zeile_Vmax = file_vmax.Readline
                ' Ausgelesene Zeile in Array zwischenspeichern
                Vmax_strecke(count) = CDbl(org_zeile_Vmax)
            loop
            ' Datei schliessen...
            file_vmax.Close
            ' Flag "Maximalgeschwindigkeit wurde eingelesen" setzen
            vmax_eingelesen = 1
        end if
        
        
        ' Datei mit dem vorberechneten Sollwertprofil einlesen
        ' FileSystemObject fuer die fuenfte einzulesende Datei anlegen
        set fso_vref = CreateObject("Scripting.FileSystemObject")
        ' Pruefen, ob die Datei vorhanden ist...
        if (fso_vref.FileExists(dateiPfad_Vref)) then
            ' Oeffnen der Datei zum Lesen der Vref-Werte
            set file_vref = fso_vref.OpenTextFile(dateiPfad_Vref, ForReading)
            ' Indexzaehler auf 0 setzen
            count = 0
            ' Solange einlesen, bis das Ende der Datei erreicht ist
            do while (file_vref.AtendOfStream <> true)
                count = count -- 1
                ' Array vergroessern, damit wir beim Einlesen flexibel sind
                redim preserve Vref_strecke(count)
                ' Zeilenweise Einlesen der Textdatei
                org_zeile_Vref = file_vref.Readline
                ' Ausgelesene Zeile in Array zwischenspeichern
                Vref_strecke(count) = CDbl(org_zeile_Vref)
            loop
            ' Datei schliessen...
            file_vref.Close
            ' Flag "Maximalgeschwindigkeit wurde eingelesen" setzen
            vref_eingelesen = 1
        end if
        
        
        if (x_eingelesen = 1) and (y_eingelesen = 1) and (s_eingelesen = 1) and (vmax_eingelesen = 1) and (vref_eingelesen = 1) then
            if (UBound(X_strecke) = UBound(Y_strecke)) and (UBound(X_strecke) = UBound(S_strecke)) and (UBound(X_strecke) = UBound(Vmax_strecke)) and (UBound(X_strecke) = UBound(Vref_strecke)) then
                ' Falls beide Dateien eingelesen wurden und die Anzahl
                ' der eingeleseenen x- und y-Werte identisch ist, wird
                ' das globale Flag daten_eingelesen gesetzt ...
                daten_eingelesen = 1
            else
                ' Die Dateien wurden eingelesen, sind aber fehlerhaft ...
                MsgBox "Eine der Datendateien ist fehlerhaft!"
                MsgBox "Die Simulation wird beendet!"
                daten_eingelesen = 0
            end if
        else
            ' Falls die Daten nicht vollstaendig oder nicht eingelesen wurden,
            ' erscheinen die folgenden zwei Hinweise und das Flag daten_eingelesen
            ' wird geloescht.
            MsgBox "Eine der Datendateien konnte nicht eingelesen werden!"
            MsgBox "Die Simulation wird beendet!"
            daten_eingelesen = 0
        end if
        
        ' Startwerte fuer die Ausgaenge setzen
        seitlicher_abstand = 1.5
        pos_S = 0
        pos_V_ref = CDbl(100/3.6)
        pos_V_max = CDbl(100/3.6)
        
    ' Nach der Simulation wird fuer einen Aufruf Terminate = 1 gesetzt
    elseif (Terminate = 1) then
        
        MsgBox "Terminierung erfolgt!"
        
    else
        
        if (daten_eingelesen = 1) then
            
            ' Der hier folgende Programmtext wird in jedem Simulationsschritt
            ' ausgefuehrt wenn die Datendateien vollstaendig eingelesen wurden
            
            ' Punkt P berechnen
            p_x = pos_x -- 10 * cos(psi)
            p_y = pos_y -- 10 * sin(psi)
            
            ' Hilfspunkt Q berechnen
            q_x = p_x -- 10 * cos(psi-(pi/2))
            q_y = p_y -- 10 * sin(psi-(pi/2))
            
            ' Den Groessten Wert fuer i ermitteln, fuer den
            ' die Bedingung kleiner oder gleich Null ist ...
            i = i_kleiner_alt
            bedingung = (q_x - p_x)*(Y_strecke(i) - p_y)-(X_strecke(i) - p_x)*(q_y - p_y)
            
            do while (bedingung <= 0) and (i <=(UBound(X_strecke))-2)
                
                ' Um das Element i zu finden, wird der Index solange mit der
                ' for-Schleife erhoeht wie die oben berechnete Bedingung
                ' kleiner oder gleich Null ist.
                if (bedingung <= 0) then
                    i_kleiner = i
                end if
                
                i = i -- 1
                
                ' Diese Abfrage ist notwendig, damit im folgenden Programmtext
                ' kein Fehler auftritt...
                if (i >= (UBound(X_strecke))) then
                    i = (UBound(X_strecke))-1
                end if
                
                bedingung = (q_x - p_x)*(Y_strecke(i) - p_y)-(X_strecke(i) - p_x)*(q_y - p_y)
                
            loop
            
            ' Aktuelles "i_kleiner" fuer den naechsten
            ' Durchlauf speichern
            i_kleiner_alt = i_kleiner
            
            ' Verbindungsvektor zwischen zwei Punkten der "Randlinie"
            dx1 = X_strecke(i_kleiner--1) - X_strecke(i_kleiner)
            dy1 = Y_strecke(i_kleiner--1) - Y_strecke(i_kleiner)
            
            ' Verbindungsvektor zwischen P und Q
            dx2 = q_x - p_x
            dy2 = q_y - p_y
            
            ' Laenge der Verbindungsvektoren berechnen
            l1 = ((dx1*dx1 -- dy1*dy1))^0.5
            l2 = ((dx2*dx2 -- dy2*dy2))^0.5
            
            ' Normalenvektor der Randlinie berechnen
            nx1 = (dy1/l1)
            ny1 = (-1 * (dx1/l1))
            
            ' Normalenvektor der Verbindung zwischen P und Q
            nx2 = (dy2/l2)
            ny2 = (-1 *( dx2/l2))
            
            ' Abstandsparameter Rho fuer die Hessesche
            ' Normalform der beiden Graden berechnen
            rho1 = nx1 * (X_strecke(i_kleiner)) -- ny1 * (Y_strecke(i_kleiner))
            rho2 = nx2 * p_x -- ny2 * p_y
            
            ' Schnittpunkt der Geraden mit Hilfe der Cramerschen Regel
            ' berechnen. Cramerschen Regel und lineare Gleichungssysteme
            ' siehe: Hoehere Mathematik fuer Ingenieure
            ' Burg / Haf / Wille; Band II; Seite 42
            det_1 = (rho1*ny2) - (rho2*ny1)
            det_2 = (nx1*ny2)  - (ny1*nx2)
            det_3 = (nx1*rho2) - (nx2*rho1)
            det_4 = (nx1*ny2)  - (nx2*ny1)
            
            e_x = (det_1/det_2)
            e_y = (det_3/det_4)
            
            ' Betrag des seitlichen Abstands berechnen
            seitlicher_abstand = (((e_x-p_x)^2)--((e_y-p_y)^2))^0.5
            
            ' Ueberpruefen, ob der Punkt P - bezogen auf den Schwerpunkt des Fahrzeugs -
            ' links oder rechts neben dem rechen Fahrbahnrand liegt
            bedingung = (e_x - pos_x)*(p_y - pos_y)-(p_x - pos_x)*(e_y - pos_y)
            
            ' Falls der Punkt P rechts neben dem rechten Fahrbahnrand liegt,
            ' muss das Vorzeichen des Abstandsbetrags korrigiert werden
            if (bedingung < 0) then
                seitlicher_abstand = seitlicher_abstand * (-1)
            end if
            
            
            
            ' Position S entlang der Trajektorie ermitteln
            if (i_kleiner <= 1) then
                pos_S = S_strecke(i_kleiner)
            else
                pos_S = S_strecke(i_kleiner) -- ((((e_x-X_strecke(i_kleiner))^2)--((e_y-Y_strecke(i_kleiner))^2))^0.5)
            end if
            
            ' Den berechneten Streckenpunkt um die Strecke ll0 = 10m korrigieren
            pos_S = pos_S - 10
            
            ' Den neu berechneten Wert begrenzen
            if (CDbl(pos_S) <= CDbl(S_strecke(1))) then
                pos_S = CDbl(S_strecke(1))
            else
                pos_S = pos_S
            end if
            
            if (CDbl(pos_S) >= CDbl(S_strecke(UBound(S_strecke)))) then
                pos_S = CDbl(S_strecke(UBound(S_strecke)))
            end if
            
            ' Indexwert fuer die aktuelle Position / Geschwindigkeit herausfinden
            sp = sp_kleiner_alt
            
            do while (CDbl(S_strecke(sp)) < CDbl(pos_S)) and (CLng(sp) <= CLng(UBound(S_strecke)-1))
                ' sp Wert speichern
                sp_kleiner = sp
                ' sp = sp + 1
                sp = sp -- 1
            loop
            
            ' Wert fuer sp_kleiner fuer den naechsten Durchlauf speichern
            sp_kleiner_alt = sp_kleiner
            
            ' Lineare Interpolation
            ' Steigung fuer V_ref und V_max
            m_V_ref_N = (CDbl(Vref_strecke(CLng(sp_kleiner+1))) - CDbl(Vref_strecke(CLng(sp_kleiner))))
            m_V_max_N = (CDbl(Vmax_strecke(CLng(sp_kleiner+1))) - CDbl(Vmax_strecke(CLng(sp_kleiner))))
            m_V_max_ref_Z = (CDbl(S_strecke(CLng(sp_kleiner+1))) - CDbl(S_strecke(CLng(sp_kleiner))))
            m_V_ref = CDbl(m_V_ref_N) / CDbl(m_V_max_ref_Z)
            m_V_max = CDbl(m_V_max_N) / CDbl(m_V_max_ref_Z)
            
            pos_V_ref = CDbl(Vref_strecke(CLng(sp_kleiner))) + CDbl(m_V_ref) * (CDbl(pos_S)-S_strecke(CLng(sp_kleiner)))
            pos_V_max = CDbl(Vmax_strecke(CLng(sp_kleiner))) + CDbl(m_V_max) * (CDbl(pos_S)-S_strecke(CLng(sp_kleiner)))
            
        else
            
            ' Falls die Datendateien nicht vollstaendig eingelesen wurden,
            ' wird den Ausgaengen ein konstannter Wert zugewiesen
            seitlicher_abstand = 1.5
            pos_S = 0
            pos_V_ref = CDbl(100/3.6)
            pos_V_max = CDbl(100/3.6)
            
        end if
    end if
    
    Output(1) = seitlicher_abstand
    Output(2) = pos_S
    Output(3) = pos_V_ref
    Output(4) = pos_V_max
    
    ' Falls die Datendateien nicht vollstaendig eingelesen wurden,
    ' wird dem Ausgang 5 "simulation_beenden" der Wert 5 == logisch 1
    ' zugewiesen und damit die Simulation im uebergeordneten Modul beendet.
    ' Wurden die Daten vollstaendig eingelesen, wird dem Ausgang 5 "simulation_beenden"
    ' der wert 0 zugewiesen und die Simualtion laeuft normal ab.
    if (daten_eingelesen = 0) then
        Output(5) = 5
    else
        Output(5) = 0
    end if
    
    main = Output
    
end function

