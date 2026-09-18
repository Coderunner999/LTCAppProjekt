

from fpdf import FPDF

class Certificate(FPDF):
    def draw_border(self):
        # Zeichnet einen eleganten, doppelten Rahmen um das Zertifikat in DUNKELBLAU
        self.set_line_width(1.5)
        self.set_draw_color(10, 45, 110)  # Elegantes Dunkelblau (#0A2D6E)
        self.rect(10, 10, 190, 277)
        
        self.set_line_width(0.5)
        self.rect(12, 12, 186, 273)
        
    def draw_corner_ribbon(self):
        # Zeichnet die obere rechte dunkelblaue Eckfahne mit Text "LTC"
        self.set_fill_color(10, 45, 110)
        self.set_draw_color(10, 45, 110)
        
        points = [
            (150, 10),  
            (170, 10),  
            (200, 40),  
            (200, 60)   
        ]
        self.polygon(points, style="F")
        
        self.set_font("Helvetica", "B", size=18)
        self.set_text_color(255, 255, 255)
        
        with self.rotation(angle=-45, x=180, y=30):
            self.text(x=174, y=32, txt="LTC")

    def draw_bottom_left_ribbon(self):
        # Zeichnet eine exakt ausgerichtete Eckfahne unten links (OHNE Text)
        self.set_fill_color(10, 45, 110)  # Dunkelblau
        self.set_draw_color(10, 45, 110)
        
        # JETZT EXAKT AN DEN RAHMEN ANGEPASST:
        # Die X-Werte starten jetzt bei 10 (Rahmenkante) statt bei 0.
        # Die Y-Werte wurden an die untere Rahmenkante (287) angepasst.
        points = [
            (10, 237),   # Start an der linken Rahmenkante
            (10, 257),   # Ende an der linken Rahmenkante
            (35, 287),   # Start an der unteren Rahmenkante
            (55, 287)    # Ende an der unteren Rahmenkante
        ]
        self.polygon(points, style="F")


def create_certificate():
    # A4 im Hochformat (Portrait)
    pdf = Certificate(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.draw_border()
    pdf.draw_corner_ribbon()       # Obere rechte Fahne mit Text
    pdf.draw_bottom_left_ribbon()  # Untere linke Fahne ohne Text
    
    # Automatischen Seitenumbruch deaktivieren für Layout-Treue
    pdf.set_auto_page_break(False)
    
    # ---- 1. ÜBERSCHRIFT (DUNKELBLAU) ----
    pdf.set_y(50)
    pdf.set_font("Helvetica", "B", size=26)
    pdf.set_text_color(10, 45, 110)
    pdf.cell(190, 10, txt="CERTIFICATE OF COMPLETION", ln=True, align="C")
    
    # ---- 2. ZWISCHENTEXT 1 (GRAU) ----
    # ---- 2. ZWISCHENTEXT 1 (GERADE UND IN ORIGINAL-GRAU) ----
    pdf.ln(15)
    # "I" (Italic) wurde entfernt, die Schriftart ist jetzt ganz normal gerade
    pdf.set_font("Helvetica", "", size=14) 
    # Exakt das gleiche elegante Grau wie bei den Punkten unten (#5A5A5A)
    pdf.set_text_color(90, 90, 90)  
    pdf.cell(190, 10, txt="The LTC platform certifies that", ln=True, align="C")

    
    # ---- 3. NAME (DUNKELBLAU) ----
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", size=24)
    pdf.set_text_color(10, 45, 110)  # Dunkelblau
    pdf.cell(190, 12, txt="Max Mustermann", ln=True, align="C")
    
    # ---- ZWISCHENTEXT 2 (ENG AN DEN NAMEN GEZOGEN) ----
    pdf.ln(2) # Minimaler Abstand nach dem Namen
    pdf.set_font("Helvetica", "", size=14) 
    pdf.set_text_color(90, 90, 90)  # Das identische Original-Grau von oben
    pdf.cell(190, 10, txt="for successful completion of", ln=True, align="C")
    
    # ---- 4. KURS-NAME (ENG AN DEN ZWISCHENTEXT GEZOGEN) ----
    pdf.ln(4) # Minimaler Abstand vor dem großen Kursnamen
    pdf.set_font("Helvetica", "B", size=24) 
    pdf.set_text_color(80, 80, 80)  
    pdf.cell(190, 12, txt="Introduction to Programming", ln=True, align="C")

    
    # ---- 5. ZWISCHENTEXT 2 (GRAU) ----
    pdf.ln(18)
    pdf.set_font("Helvetica", "", size=12)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(190, 10, txt="This certification provides:", ln=True, align="C")
    
    # ---- 6. AUFZÄHLUNGEN (BULLET POINTS IN GRAU) ----
    pdf.ln(3)
    points = [
        "Core Python and JavaScript programming concepts",
        "Experience creating simple Websites with HTML and CSS",
        "Building first projects with Python and AI"
    ]
    
    pdf.set_font("Helvetica", "", size=12)
    pdf.set_text_color(90, 90, 90)
    
    for point in points:
        pdf.set_x(45)
        pdf.cell(8, 8, txt=chr(149), ln=False)
        pdf.cell(120, 8, txt=point, ln=True)
        
    # PDF speichern
    pdf.output("LTC Introduction Certificate.pdf")
    print("Zertifikat mit symmetrischen Eckfahnen erfolgreich generiert!")

if __name__ == "__main__":
    create_certificate()
