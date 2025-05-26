# DZ Self-Assessment Tool – Multi-Page Survey with Navigation

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="DZ Self-Assessment", layout="centered")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

if 'answers' not in st.session_state:
    st.session_state.answers = {}

if 'dimension_scores' not in st.session_state:
    st.session_state.dimension_scores = {}

# Page configuration
pages = [
    {"title": "Willkommen", "icon": "🏠"},
    {"title": "Anwendungspotenzial", "icon": "🎯"},
    {"title": "Strategischer Nutzen", "icon": "📈"},
    {"title": "Hemmnisse & Herausforderungen", "icon": "⚠️"},
    {"title": "Voraussetzungen & Erfolgsfaktoren", "icon": "✅"},
    {"title": "Auswertung", "icon": "📊"}
]

def calculate_dimension_scores():
    """Calculate scores for all dimensions based on current answers"""
    scores = {}

    # Dimension 1: Anwendungspotenzial
    if any(key.startswith('anwendung_') for key in st.session_state.answers):
        anwendung_scores = {}
        
        # Basic sector score
        sektor = st.session_state.answers.get('anwendung_1_1', '')
        sektor_score = {
            "Produktion / Fertigung": 3,
            "Medizintechnik": 3,
            "Luft- und Raumfahrt": 3,
            "Sonstige stark regulierte Branchen": 3,
            "Bauwesen": 1,
            "Landwirtschaft": 0,
            "Sonstige": 0
        }.get(sektor, 0)
        anwendung_scores["1.1"] = sektor_score

        # Conditional questions
        if sektor in ["Medizintechnik", "Luft- und Raumfahrt", "Sonstige stark regulierte Branchen"]:
            anwendung_scores["1.1.1"] = 3 if st.session_state.answers.get('anwendung_1_1_1') == "Ja" else 0
        if sektor == "Landwirtschaft":
            agri = st.session_state.get('anwendung_1_1_2_multiselect', [])
            anwendung_scores["1.1.2"] = 3 if agri else 0
        if sektor == "Produktion / Fertigung" or anwendung_scores.get("1.1.1") == 3:
            choice_113 = st.session_state.answers.get('anwendung_1_1_3', '')
            anwendung_scores["1.1.3"] = 3 if choice_113 == "Konstant Hohes, stabiles Volumen" else 0

        # Standard questions (always calculate)
        bereich = st.session_state.get('anwendung_1_2_multiselect', [])
        if "Keine" in bereich or not bereich:
            anwendung_scores["1.2"] = 0
        elif len(bereich) == 1:
            anwendung_scores["1.2"] = 1
        elif len(bereich) <= 3:
            anwendung_scores["1.2"] = 3
        else:
            anwendung_scores["1.2"] = 5

        anwendung_scores["1.3"] = {
            "Nicht standardisiert": 0,
            "Eher wenig standardisiert": 1,
            "Teilweise standardisiert": 2,
            "Weitgehend standardisiert": 3,
            "Vollständig standardisiert": 4
        }.get(st.session_state.answers.get('anwendung_1_3', ''), 0)

        anwendung_scores["1.4"] = {
            "Sehr gering": 0,
            "Gering": 1,
            "Mittel": 2,
            "Hoch": 3,
            "Sehr hoch": 4
        }.get(st.session_state.answers.get('anwendung_1_4', ''), 0)

        anwendung_scores["1.5"] = {
            "Nein": 0,
            "Nicht sicher": 2,
            "Ja": 4
        }.get(st.session_state.answers.get('anwendung_1_5', ''), 0)

        anwendung_scores["1.6"] = {
            "Nie": 0,
            "Selten": 1,
            "Gelegentlich": 2,
            "Häufig": 3,
            "Sehr häufig": 4
        }.get(st.session_state.answers.get('anwendung_1_6', ''), 0)

        # Calculate max score dynamically
        max_score_anwendung = 3  # 1.1
        if sektor in ["Medizintechnik", "Luft- und Raumfahrt", "Sonstige stark regulierte Branchen"]:
            max_score_anwendung += 3  # 1.1.1
        if sektor == "Landwirtschaft":
            max_score_anwendung += 3  # 1.1.2
        if sektor == "Produktion / Fertigung" or anwendung_scores.get("1.1.1") == 3:
            max_score_anwendung += 3  # 1.1.3
        # Standard questions always count
        max_score_anwendung += 5 + 4 + 4 + 4 + 4  # 1.2 bis 1.6

        scores["Anwendungspotenzial"] = sum(anwendung_scores.values()) / max_score_anwendung * 100
    
    # Dimension 2: Strategischer Nutzen
    if any(key.startswith('strategisch_') for key in st.session_state.answers):
        strategisch_scores = {}
        
        strategisch_scores["2.1"] = {
            "Kein Potenzial": 0,
            "Geringes": 1,
            "Mittleres": 2,
            "Hohes": 3,
            "Sehr hohes": 4
        }.get(st.session_state.answers.get('strategisch_2_1', ''), 0)

        strategisch_scores["2.2"] = {
            "Nicht wichtig": 0,
            "Eher nicht": 1,
            "Mittel": 2,
            "Wichtig": 3,
            "Sehr wichtig": 4
        }.get(st.session_state.answers.get('strategisch_2_2', ''), 0)

        strategisch_scores["2.3"] = {
            "Keine": 0,
            "Geringe": 1,
            "Mittlere": 2,
            "Hohe": 3,
            "Sehr hohe": 4
        }.get(st.session_state.answers.get('strategisch_2_3', ''), 0)

        strategisch_scores["2.4"] = {
            "Gar nicht": 0,
            "Eher nicht": 1,
            "Teilweise": 2,
            "Gut": 3,
            "Sehr gut": 4
        }.get(st.session_state.answers.get('strategisch_2_4', ''), 0)

        strategisch_scores["2.5"] = {
            "Nein": 0,
            "Teilweise": 2,
            "Ja": 4
        }.get(st.session_state.answers.get('strategisch_2_5', ''), 0)
        
        scores["Strategischer Nutzen"] = sum(strategisch_scores.values()) / 20 * 100
    
    # Dimension 3: Hemmnisse
    if any(key.startswith('hemmnisse_') for key in st.session_state.answers):
        hemmnisse_scores = {}
        
        hemmnisse_scores["3.1"] = {
            "Gar nicht": 0,
            "Kaum": 1,
            "Teilweise": 2,
            "Weitgehend": 3,
            "Vollständig": 4
        }.get(st.session_state.answers.get('hemmnisse_3_1', ''), 0)

        hemmnisse_scores["3.2"] = {
            "Stimme nicht zu": 0,
            "Eher nicht": 1,
            "Teils/Teils": 2,
            "Eher ja": 3,
            "Stimme voll zu": 4
        }.get(st.session_state.answers.get('hemmnisse_3_2', ''), 0)

        hemmnisse_scores["3.3"] = {
            "Überhaupt nicht": 0,
            "Kaum": 1,
            "Teilweise": 2,
            "Gut": 3,
            "Sehr klar": 4
        }.get(st.session_state.answers.get('hemmnisse_3_3', ''), 0)

        hemmnisse_scores["3.4"] = {
            "Stimme voll zu": 0,
            "Eher ja": 1,
            "Teils/Teils": 2,
            "Eher nicht": 3,
            "Stimme nicht zu": 4
        }.get(st.session_state.answers.get('hemmnisse_3_4', ''), 0)
        
        hemmnisse_scores["3.5"] = {
            "Gar nicht sicher": 0,
            "Wenig": 1,
            "Teilweise": 2,
            "Ziemlich": 3,
            "Sehr sicher": 4
        }.get(st.session_state.answers.get('hemmnisse_3_5', ''), 0)
        
        scores["Hemmnisse"] = sum(hemmnisse_scores.values()) / 20 * 100
    
    # Dimension 4: Voraussetzungen
    if any(key.startswith('voraussetzungen_') for key in st.session_state.answers):
        voraussetzungen_scores = {}
        
        voraussetzungen_scores["4.1"] = {
            "Gar nicht": 0,
            "Einzelne Schritte": 1,
            "Teilweise integriert": 2,
            "Weitgehend integriert": 3,
            "Vollständig integriert": 4
        }.get(st.session_state.answers.get('voraussetzungen_4_1', ''), 0)

        voraussetzungen_scores["4.2"] = {
            "Überhaupt nicht": 0,
            "Gering": 1,
            "Teilweise": 2,
            "Gut": 3,
            "Sehr gut": 4
        }.get(st.session_state.answers.get('voraussetzungen_4_2', ''), 0)

        voraussetzungen_scores["4.3"] = {
            "Stimme nicht zu": 0,
            "Eher nicht": 1,
            "Teils/Teils": 2,
            "Eher ja": 3,
            "Stimme voll zu": 4
        }.get(st.session_state.answers.get('voraussetzungen_4_3', ''), 0)
        
        voraussetzungen_scores["4.4"] = 4 if st.session_state.answers.get('voraussetzungen_4_4') == "Ja" else 0
        voraussetzungen_scores["4.5"] = 4 if st.session_state.answers.get('voraussetzungen_4_5') == "Ja" else 0
        
        scores["Voraussetzungen"] = sum(voraussetzungen_scores.values()) / 20 * 100
    
    st.session_state.dimension_scores = scores

def show_navigation():
    """Display navigation buttons"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page > 0:
            if st.button("← Zurück", use_container_width=True, type="secondary"):
                st.session_state.current_page -= 1
                st.rerun()
    
    with col2:
        # Progress bar
        progress = st.session_state.current_page / (len(pages) - 1)
        st.progress(progress, text=f"Schritt {st.session_state.current_page + 1} von {len(pages)}")
    
    with col3:
        if st.session_state.current_page < len(pages) - 1:
            if st.button("Weiter →", use_container_width=True, type="primary"):
                st.session_state.current_page += 1
                st.rerun()

def show_welcome_page():
    """Show welcome page"""
    st.title("🏠 Self-Assessment-Tool: Digitale Zwillinge in KMU")
    
    st.markdown("""
    ### Willkommen zum DZ Self-Assessment!
    
    Dieses Tool hilft Ihnen dabei, das Potenzial digitaler Zwillinge für Ihr Unternehmen zu bewerten.
    
    **Was Sie erwartet:**
    - 📝 4 Themenbereiche mit gezielten Fragen
    - ⏱️ Bearbeitungszeit: ca. 5-10 Minuten
    - 📊 Individuelle Auswertung mit Radar-Diagramm
    - 💡 Konkrete Handlungsempfehlungen
    
    **Die 4 Dimensionen:**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("🎯 **Anwendungspotenzial**\nEignung Ihres Unternehmens")
        st.info("⚠️ **Hemmnisse & Herausforderungen**\nBarrieren identifizieren")
    
    with col2:
        st.info("📈 **Strategischer Nutzen**\nWertschöpfung und Ziele")
        st.info("✅ **Voraussetzungen & Erfolgsfaktoren**\nIhre Ausgangslage")
    
    st.markdown("---")
    st.markdown("**Klicken Sie auf 'Weiter', um zu beginnen!**")

def show_anwendungspotenzial_page():
    """Show application potential questions"""
    st.title("🎯 Anwendungspotenzial")
    st.markdown("*Bewertung der grundsätzlichen Eignung Ihres Unternehmens für digitale Zwillinge*")
    
    with st.container():
        st.markdown("#### 🏭 Sektor und Branche")
        sektor_options = ["Produktion / Fertigung", "Medizintechnik", "Luft- und Raumfahrt",
                          "Sonstige stark regulierte Branchen", "Landwirtschaft", "Bauwesen", "Sonstige"]
        sektor_value = st.session_state.answers.get('anwendung_1_1')
        sektor_index = sektor_options.index(sektor_value) if sektor_value in sektor_options else None
        sektor = st.radio(
            "In welchem der folgenden Sektoren ist Ihr Unternehmen primär tätig?",
            sektor_options,
            key="anwendung_1_1_radio",
            index=sektor_index
        )
        if sektor is not None:
            st.session_state.answers['anwendung_1_1'] = sektor
        
        # Conditional questions based on sector
        if sektor in ["Medizintechnik", "Luft- und Raumfahrt", "Sonstige stark regulierte Branchen"]:
            produktion_options = ["Ja", "Nein"]
            produktion_value = st.session_state.answers.get('anwendung_1_1_1')
            produktion_index = produktion_options.index(produktion_value) if produktion_value in produktion_options else None
            produktion = st.radio(
                "Produziert Ihr Unternehmen selbst?",
                produktion_options,
                key="anwendung_1_1_1_radio",
                index=produktion_index
            )
            if produktion is not None:
                st.session_state.answers['anwendung_1_1_1'] = produktion
            
        if sektor == "Landwirtschaft":
            agri_options = ["Zonenbasierte Feldbewirtschaftung", "Automatisierte Gewächshaussteuerung", 
                            "Monitoring Tierverhalten / Tiergesundheit", "Frühwarnsysteme für Pflanzenkrankheiten",
                            "Smarte Maschinensteuerung (Traktor/Drohne)", "Sensorbasierte Entscheidungsunterstützung",
                            "Digitale Nachweissysteme (z. B. Zertifizierung)"]
            agri_value = st.session_state.answers.get('anwendung_1_1_2', [])
            agri_index = [agri_options.index(a) for a in agri_value if a in agri_options]
            agri = st.multiselect(
                "Welche der folgenden Technologien oder Anwendungen werden in Ihrem Betrieb bereits eingesetzt?",
                agri_options,
                key="anwendung_1_1_2_multiselect"
            )
        
        if (sektor == "Produktion / Fertigung" or 
            (sektor in ["Medizintechnik", "Luft- und Raumfahrt", "Sonstige stark regulierte Branchen"] and 
             st.session_state.answers.get('anwendung_1_1_1') == "Ja")):
            auftragslage_options = ["Konstant Hohes, stabiles Volumen", "Mittelmäßig / schwankend"]
            auftragslage_value = st.session_state.answers.get('anwendung_1_1_3')
            auftragslage_index = auftragslage_options.index(auftragslage_value) if auftragslage_value in auftragslage_options else None
            auftragslage = st.radio(
                "Wie stabil und planbar würden Sie Ihre Auftragslage einschätzen?",
                auftragslage_options,
                key="anwendung_1_1_3_radio",
                index=auftragslage_index
            )
            if auftragslage is not None:
                st.session_state.answers['anwendung_1_1_3'] = auftragslage
        
        st.markdown("#### 📊 Digitale Datennutzung")
        # Question 1.2
        bereich_options = ["Produktentwicklung", "Produktion", "Wartung & Service", "Logistik", "Qualitätssicherung", "Keine"]
        bereich = st.multiselect(
            "In welchen betrieblichen Bereichen nutzen Sie bereits digitale oder sensorbasierte Daten?",
            bereich_options,
            key="anwendung_1_2_multiselect"
        )
        
        st.markdown("#### ⚙️ Prozesse und Komplexität")
        # Question 1.3
        standardisierung_options = ["Nicht standardisiert", "Eher wenig standardisiert", "Teilweise standardisiert", 
                                     "Weitgehend standardisiert", "Vollständig standardisiert"]
        standardisierung_value = st.session_state.answers.get('anwendung_1_3')
        standardisierung_index = standardisierung_options.index(standardisierung_value) if standardisierung_value in standardisierung_options else None
        standardisierung = st.radio(
            "Wie standardisiert und wiederholbar sind die betrieblichen Prozesse in Ihrem Unternehmen?",
            standardisierung_options,
            key="anwendung_1_3_radio",
            index=standardisierung_index
        )
        st.session_state.answers['anwendung_1_3'] = standardisierung
        
        # Question 1.4
        komplexitaet_options = ["Sehr gering", "Gering", "Mittel", "Hoch", "Sehr hoch"]
        komplexitaet_value = st.session_state.answers.get('anwendung_1_4')
        komplexitaet_index = komplexitaet_options.index(komplexitaet_value) if komplexitaet_value in komplexitaet_options else None
        komplexitaet = st.radio(
            "Wie hoch ist die Komplexität Ihrer Produkte oder Prozesse (z.B. Variantenvielfalt, Individualisierung, hoher Planungsaufwand)?",
            komplexitaet_options,
            key="anwendung_1_4_radio",
            index=komplexitaet_index
        )
        st.session_state.answers['anwendung_1_4'] = komplexitaet
        
        st.markdown("#### 🎯 Digitale Simulation")
        # Question 1.5
        simulation_options = ["Nein", "Nicht sicher", "Ja"]
        simulation_value = st.session_state.answers.get('anwendung_1_5')
        simulation_index = simulation_options.index(simulation_value) if simulation_value in simulation_options else None
        simulation = st.radio(
            "Gibt es Prozesse oder Vorgänge, die sich grundsätzlich für eine digitale Abbildung oder Simulation eignen (z.B. Maschinenverhalten, Abläufe)?",
            simulation_options,
            key="anwendung_1_5_radio",
            index=simulation_index
        )
        st.session_state.answers['anwendung_1_5'] = simulation
        
        # Question 1.6
        probleme_options = ["Nie", "Selten", "Gelegentlich", "Häufig", "Sehr häufig"]
        probleme_value = st.session_state.answers.get('anwendung_1_6')
        probleme_index = probleme_options.index(probleme_value) if probleme_value in probleme_options else None
        probleme = st.radio(
            "Wie häufig treten in Ihrem Unternehmen wiederkehrende Probleme auf, deren Ursachen grundsätzlich datenbasiert analysiert werden könnten (z.B. Ausfälle, Schwankungen)?",
            probleme_options,
            key="anwendung_1_6_radio",
            index=probleme_index
        )
        st.session_state.answers['anwendung_1_6'] = probleme

def show_strategischer_nutzen_page():
    """Show strategic value questions"""
    st.title("📈 Strategischer Nutzen")
    st.markdown("*Bewertung der strategischen Bedeutung und des Wertschöpfungspotenzials*")
    
    with st.container():
        st.markdown("#### ⚡ Effizienzpotenzial")
        # Question 2.1
        effizienz_options = ["Kein Potenzial", "Geringes", "Mittleres", "Hohes", "Sehr hohes"]
        effizienz_value = st.session_state.answers.get('strategisch_2_1')
        effizienz_index = effizienz_options.index(effizienz_value) if effizienz_value in effizienz_options else None
        effizienz = st.radio(
            "Wo sehen Sie im Unternehmen aktuell Potenzial für Effizienzsteigerung z.B. durch bessere Planung, kürzere Wege oder gezieltere Abläufe?",
            effizienz_options,
            key="strategisch_2_1_radio",
            index=effizienz_index
        )
        st.session_state.answers['strategisch_2_1'] = effizienz
        
        st.markdown("#### 🌱 Ressourcenoptimierung")
        # Question 2.2
        ressourcen_options = ["Nicht wichtig", "Eher nicht", "Mittel", "Wichtig", "Sehr wichtig"]
        ressourcen_value = st.session_state.answers.get('strategisch_2_2')
        ressourcen_index = ressourcen_options.index(ressourcen_value) if ressourcen_value in ressourcen_options else None
        ressourcen = st.radio(
            "Wie wichtig ist es für Ihr Unternehmen, Ressourcen wie Energie, Material oder Zeit gezielter einzusetzen durch digitale Zwillinge?",
            ressourcen_options,
            key="strategisch_2_2_radio",
            index=ressourcen_index
        )
        st.session_state.answers['strategisch_2_2'] = ressourcen
        
        st.markdown("#### 🎯 Qualitätssicherung")
        # Question 2.3
        qualitaet_options = ["Keine", "Geringe", "Mittlere", "Hohe", "Sehr hohe"]
        qualitaet_value = st.session_state.answers.get('strategisch_2_3')
        qualitaet_index = qualitaet_options.index(qualitaet_value) if qualitaet_value in qualitaet_options else None
        qualitaet = st.radio(
            "Welche Rolle spielt Qualitätssicherung durch datenbasierte Überwachung oder Analyse in Ihrem Unternehmen?",
            qualitaet_options,
            key="strategisch_2_3_radio",
            index=qualitaet_index
        )
        st.session_state.answers['strategisch_2_3'] = qualitaet
        
        st.markdown("#### 🗺️ Strategische Einordnung")
        # Question 2.4
        strategie_options = ["Gar nicht", "Eher nicht", "Teilweise", "Gut", "Sehr gut"]
        strategie_value = st.session_state.answers.get('strategisch_2_4')
        strategie_index = strategie_options.index(strategie_value) if strategie_value in strategie_options else None
        strategie = st.radio(
            "Wie gut lässt sich das Thema digitale Zwillinge in Ihre bestehende Digitalstrategie oder Zielbilder einordnen?",
            strategie_options,
            key="strategisch_2_4_radio",
            index=strategie_index
        )
        st.session_state.answers['strategisch_2_4'] = strategie
        
        st.markdown("#### 🚀 Neue Geschäftsmodelle")
        # Question 2.5
        services_options = ["Nein", "Teilweise", "Ja"]
        services_value = st.session_state.answers.get('strategisch_2_5')
        services_index = services_options.index(services_value) if services_value in services_options else None
        services = st.radio(
            "Erwägen Sie aktuell die Einführung neuer digitaler Services oder Geschäftsmodelle?",
            services_options,
            key="strategisch_2_5_radio",
            index=services_index
        )
        st.session_state.answers['strategisch_2_5'] = services

def show_hemmnisse_page():
    """Show barriers and challenges questions"""
    st.title("⚠️ Hemmnisse & Herausforderungen")
    st.markdown("*Identifikation von Barrieren und Herausforderungen*")
    
    with st.container():
        st.markdown("#### 💾 Datenstruktur")
        # Question 3.1
        daten_options = ["Gar nicht", "Kaum", "Teilweise", "Weitgehend", "Vollständig"]
        daten_value = st.session_state.answers.get('hemmnisse_3_1')
        daten_index = daten_options.index(daten_value) if daten_value in daten_options else None
        daten = st.radio(
            "Wie gut sind Ihre internen Datenquellen strukturiert und zugänglich? (einheitliche Datenbanken vs. Excel-Listen und lokale Speicherung)",
            daten_options,
            key="hemmnisse_3_1_radio",
            index=daten_index
        )
        st.session_state.answers['hemmnisse_3_1'] = daten
        
        st.markdown("#### 💰 Wirtschaftlichkeit")
        # Question 3.2
        roi_options = ["Stimme nicht zu", "Eher nicht", "Teils/Teils", "Eher ja", "Stimme voll zu"]
        roi_value = st.session_state.answers.get('hemmnisse_3_2')
        roi_index = roi_options.index(roi_value) if roi_value in roi_options else None
        roi = st.radio(
            "Wir haben eine klare Vorstellung davon, wie sich Investitionen in digitale Technologien wirtschaftlich auszahlen können (z. B. ROI, Effizienzgewinne)",
            roi_options,
            key="hemmnisse_3_2_radio",
            index=roi_index
        )
        st.session_state.answers['hemmnisse_3_2'] = roi
        
        st.markdown("#### 👥 Organisation")
        # Question 3.3
        zustaendigkeiten_options = ["Überhaupt nicht", "Kaum", "Teilweise", "Gut", "Sehr klar"]
        zustaendigkeiten_value = st.session_state.answers.get('hemmnisse_3_3')
        zustaendigkeiten_index = zustaendigkeiten_options.index(zustaendigkeiten_value) if zustaendigkeiten_value in zustaendigkeiten_options else None
        zustaendigkeiten = st.radio(
            "Wie klar geregelt sind Zuständigkeiten und Verantwortung bei Digitalisierungsprojekten in Ihrem Unternehmen?",
            zustaendigkeiten_options,
            key="hemmnisse_3_3_radio",
            index=zustaendigkeiten_index
        )
        st.session_state.answers['hemmnisse_3_3'] = zustaendigkeiten
        
        st.markdown("#### 🤔 Interne Akzeptanz")
        # Question 3.4
        vorbehalte_options = ["Stimme voll zu", "Eher ja", "Teils/Teils", "Eher nicht", "Stimme nicht zu"]
        vorbehalte_value = st.session_state.answers.get('hemmnisse_3_4')
        vorbehalte_index = vorbehalte_options.index(vorbehalte_value) if vorbehalte_value in vorbehalte_options else None
        vorbehalte = st.radio(
            "In unserem Unternehmen spielen interne Vorbehalte oder Unsicherheiten (z. B. Skepsis, Überforderung, Ablehnung) gegenüber neuen digitalen Lösungen eine große Rolle.",
            vorbehalte_options,
            key="hemmnisse_3_4_radio",
            index=vorbehalte_index
        )
        st.session_state.answers['hemmnisse_3_4'] = vorbehalte
        
        st.markdown("#### 🔒 Datenschutz & Recht")
        # Question 3.5
        datenschutz_options = ["Gar nicht sicher", "Wenig", "Teilweise", "Ziemlich", "Sehr sicher"]
        datenschutz = st.radio(
            "Wie sicher fühlen Sie sich im Umgang mit Fragen zu Datenschutz und rechtlichen Anforderungen bei digitalen Systemen?",
            ["Gar nicht sicher", "Wenig", "Teilweise", "Ziemlich", "Sehr sicher"],
            key="hemmnisse_3_5_radio",
            index=["Gar nicht sicher", "Wenig", "Teilweise", "Ziemlich", "Sehr sicher"].index(
                st.session_state.answers.get('hemmnisse_3_5', "Gar nicht sicher"))
        )
        st.session_state.answers['hemmnisse_3_5'] = datenschutz

def show_voraussetzungen_page():
    """Show prerequisites and success factors questions"""
    st.title("✅ Voraussetzungen & Erfolgsfaktoren")
    st.markdown("*Bewertung Ihrer aktuellen Ausgangslage und Erfolgsfaktoren*")
    
    with st.container():
        st.markdown("#### 🏗️ Wertschöpfung")
        # Question 4.1
        wertschoepfung_options = ["Gar nicht", "Einzelne Schritte", "Teilweise integriert", "Weitgehend integriert", "Vollständig integriert"]
        wertschoepfung_value = st.session_state.answers.get('voraussetzungen_4_1')
        wertschoepfung_index = wertschoepfung_options.index(wertschoepfung_value) if wertschoepfung_value in wertschoepfung_options else None
        wertschoepfung = st.radio(
            "In welchem Umfang deckt Ihr Unternehmen eigene Wertschöpfungsschritte ab – z. B. Entwicklung, Produktion, Vertrieb – für ein Produkt oder System?",
            wertschoepfung_options,
            key="voraussetzungen_4_1_radio",
            index=wertschoepfung_index
        )
        if wertschoepfung is not None:
            st.session_state.answers['voraussetzungen_4_1'] = wertschoepfung
        
        st.markdown("#### 🔗 IT-Integration")
        # Question 4.2
        it_vernetzung_options = ["Überhaupt nicht", "Gering", "Teilweise", "Gut", "Sehr gut"]
        it_vernetzung_value = st.session_state.answers.get('voraussetzungen_4_2')
        it_vernetzung_index = it_vernetzung_options.index(it_vernetzung_value) if it_vernetzung_value in it_vernetzung_options else None
        it_vernetzung = st.radio(
            "Wie gut sind Ihre bestehenden IT- und Datensysteme miteinander vernetzt und interoperabel (z. B. ERP, Maschinen, Sensoren)?",
            it_vernetzung_options,
            key="voraussetzungen_4_2_radio",
            index=it_vernetzung_index
        )
        if it_vernetzung is not None:
            st.session_state.answers['voraussetzungen_4_2'] = it_vernetzung
        
        st.markdown("#### 👔 Führungsunterstützung")
        # Question 4.3
        fuehrung_options = ["Stimme nicht zu", "Eher nicht", "Teils/Teils", "Eher ja", "Stimme voll zu"]
        fuehrung_value = st.session_state.answers.get('voraussetzungen_4_3')
        fuehrung_index = fuehrung_options.index(fuehrung_value) if fuehrung_value in fuehrung_options else None
        fuehrung = st.radio(
            "Die Führungsebene unseres Unternehmens unterstützt aktiv die Umsetzung digitaler und innovativer Technologien.",
            fuehrung_options,
            key="voraussetzungen_4_3_radio",
            index=fuehrung_index
        )
        if fuehrung is not None:
            st.session_state.answers['voraussetzungen_4_3'] = fuehrung
        
        st.markdown("#### 🧪 Erfahrung & Kompetenzen")
        # Question 4.4
        pilotprojekte_options = ["Ja", "Nein"]
        pilotprojekte_value = st.session_state.answers.get('voraussetzungen_4_4')
        pilotprojekte_index = pilotprojekte_options.index(pilotprojekte_value) if pilotprojekte_value in pilotprojekte_options else None
        pilotprojekte = st.radio(
            "Wir haben bereits erfolgreich mit kleineren digitalen Projekten oder Pilotlösungen begonnen.",
            pilotprojekte_options,
            key="voraussetzungen_4_4_radio",
            index=pilotprojekte_index
        )
        if pilotprojekte is not None:
            st.session_state.answers['voraussetzungen_4_4'] = pilotprojekte
        
        # Question 4.5
        kompetenzen_options = ["Ja", "Nein"]
        kompetenzen_value = st.session_state.answers.get('voraussetzungen_4_5')
        kompetenzen_index = kompetenzen_options.index(kompetenzen_value) if kompetenzen_value in kompetenzen_options else None
        kompetenzen = st.radio(
            "Wir verfügen über interne Kompetenzen oder externe Partner, die uns beim Thema digitale Zwillinge unterstützen können.",
            kompetenzen_options,
            key="voraussetzungen_4_5_radio",
            index=kompetenzen_index
        )
        if kompetenzen is not None:
            st.session_state.answers['voraussetzungen_4_5'] = kompetenzen

def show_results_page():
    """Show results and radar chart"""
    st.title("📊 Ihre Auswertung")
    
    # Calculate scores
    calculate_dimension_scores()
    
    if not st.session_state.dimension_scores:
        st.warning("⚠️ Bitte beantworten Sie zunächst alle Fragen.")
        if st.button("🔄 Zur ersten Frage", type="primary"):
            st.session_state.current_page = 1
            st.rerun()
        return
    
    # Overall score
    gesamt_score = sum(st.session_state.dimension_scores.values()) / len(st.session_state.dimension_scores)
    
    # Display overall result with enhanced styling
    st.markdown("### Gesamtergebnis")

    if gesamt_score < 40:
        st.error(f"**Gesamtscore: {gesamt_score:.1f}%** – Geringe Eignung für den Einsatz digitaler Zwillinge")
        st.markdown("""
        **💡 Empfehlung:** Digitale Zwillinge sind zum jetzigen Zeitpunkt noch nicht optimal für Ihr Unternehmen geeignet. 
        Konzentrieren Sie sich zunächst auf die Grundlagen der Digitalisierung wie Datenstrukturierung und Prozessstandardisierung.
        """)
    elif gesamt_score < 70:
        st.warning(f"**Gesamtscore: {gesamt_score:.1f}%** – Eingeschränktes Potenzial – Vertiefung empfehlenswert")
        st.markdown("""
        **💡 Empfehlung:** Ihr Unternehmen zeigt Potenzial für digitale Zwillinge, aber es gibt noch Verbesserungsbereiche. 
        Eine schrittweise Herangehensweise mit gezielten Pilotprojekten wird empfohlen.
        """)
    else:
        st.success(f"**Gesamtscore: {gesamt_score:.1f}%** – Hohes Potenzial – Vertiefte Betrachtung empfehlenswert")
        st.markdown("""
        **💡 Empfehlung:** Ihr Unternehmen ist gut für den Einsatz digitaler Zwillinge geeignet. 
        Sie können mit konkreten Umsetzungsprojekten beginnen und strategische Partnerschaften eingehen.
        """)
    
    # Detailed scores with improved layout
    st.markdown("### 📋 Detaillierte Bewertung")
    
    col1, col2 = st.columns(2)
    
    dimension_icons = {
        "Anwendungspotenzial": "🎯",
        "Strategischer Nutzen": "📈", 
        "Hemmnisse": "⚠️",
        "Voraussetzungen": "✅"
    }
    
    for i, (dimension, score) in enumerate(st.session_state.dimension_scores.items()):
        col = col1 if i % 2 == 0 else col2
        with col:
            icon = dimension_icons.get(dimension, "📊")
            if score >= 70:
                st.success(f"{icon} **{dimension}**: {score:.1f}%")
            elif score >= 40:
                st.warning(f"{icon} **{dimension}**: {score:.1f}%")
            else:
                st.error(f"{icon} **{dimension}**: {score:.1f}%")

    # Enhanced Radar chart
    st.markdown("### 🎯 Radar-Diagramm")

    # Color based on overall score
    if gesamt_score < 40:
        chart_color = "#e45649"  # Red
        fill_color = "#e45649"
    elif gesamt_score < 70:
        chart_color = "#f2c96d"  # Yellow
        fill_color = "#f2c96d"
    else:
        chart_color = "#31c69e"  # Green
        fill_color = "#31c69e"

    labels = list(st.session_state.dimension_scores.keys())
    values = [v / 100 for v in st.session_state.dimension_scores.values()]
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color=chart_color, linewidth=4)
    ax.fill(angles, values, color=fill_color, alpha=0.3)
    ax.set_ylim(0, 1)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])

    # Enhanced label positioning
    label_positions = {
        "Anwendungspotenzial": 1.35,
        "Strategischer Nutzen": 1.10,
        "Hemmnisse": 1.20,
        "Voraussetzungen": 1.10
    }

    for angle, label in zip(angles[:-1], labels):
        distance = label_positions.get(label, 1.15)
        ax.text(angle, distance, label, rotation=0, ha='center', va='center', 
                fontsize=14, weight='bold', color='#1f1f1f')
    
    # Add percentage labels inside the chart
    for angle, value in zip(angles[:-1], values[:-1]):
        if value > 0.15:  # Only show if value is significant enough
            ax.text(angle, value/2, f'{value*100:.0f}%', ha='center', va='center', 
                    fontsize=11, color='white', weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=chart_color, alpha=0.8))
    
    # Add grid lines
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')

    st.pyplot(fig)
    
    # Enhanced action recommendations
    st.markdown("### 💡 Ihre nächsten Schritte")
    
    lowest_dimension = min(st.session_state.dimension_scores.items(), key=lambda x: x[1])
    highest_dimension = max(st.session_state.dimension_scores.items(), key=lambda x: x[1])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **💪 Ihre Stärke**
        
        {dimension_icons.get(highest_dimension[0], '📊')} **{highest_dimension[0]}**
        
        Score: {highest_dimension[1]:.1f}%
        
        Nutzen Sie diese Stärke als Ausgangspunkt für weitere Digitalisierungsschritte.
        """)
    
    with col2:
        st.warning(f"""
        **🎯 Verbesserungspotenzial**
        
        {dimension_icons.get(lowest_dimension[0], '📊')} **{lowest_dimension[0]}**
        
        Score: {lowest_dimension[1]:.1f}%
        
        Hier liegt das größte Verbesserungspotenzial für Ihr Unternehmen.
        """)
    
    st.markdown("#### 🚀 Konkrete Handlungsempfehlungen")
    
    if lowest_dimension[0] == "Anwendungspotenzial":
        st.markdown("""
        - 📋 **Prozessstandardisierung:** Überprüfen Sie Ihre Prozesse auf Standardisierungsmöglichkeiten
        - 📊 **Datenerfassung:** Identifizieren Sie datengetriebene Anwendungsfälle in Ihrem Unternehmen
        - 🔍 **Komplexitätsanalyse:** Bewerten Sie die Komplexität Ihrer Produkte und Prozesse systematisch
        - 🎯 **Simulationspotenzial:** Prüfen Sie, welche Prozesse sich für digitale Abbildung eignen
        """)
    elif lowest_dimension[0] == "Strategischer Nutzen":
        st.markdown("""
        - 🗺️ **Digitalstrategie:** Entwickeln Sie eine klare, langfristige Digitalstrategie
        - ⚡ **Effizienzanalyse:** Definieren Sie konkrete Effizienzpotenziale in Ihrem Unternehmen
        - 🌱 **Ressourcenoptimierung:** Bewerten Sie Einsparpotenziale bei Energie, Material und Zeit
        - 🚀 **Geschäftsmodelle:** Erkunden Sie neue digitale Services und Geschäftsmodelle
        """)
    elif lowest_dimension[0] == "Hemmnisse":
        st.markdown("""
        - 💾 **Datenmanagement:** Strukturieren und zentralisieren Sie Ihre Datenlandschaft
        - 💰 **ROI-Definition:** Definieren Sie klare Kennzahlen für den Return on Investment
        - 👥 **Organisationsstruktur:** Schaffen Sie klare Verantwortlichkeiten für Digitalisierung
        - 🎓 **Change Management:** Reduzieren Sie interne Vorbehalte durch Schulung und Kommunikation
        """)
    else:  # Voraussetzungen
        st.markdown("""
        - 🔗 **System-Integration:** Verbessern Sie die Vernetzung Ihrer IT- und Datensysteme
        - 🎓 **Kompetenzaufbau:** Stärken Sie digitale Kompetenzen intern oder über Partner
        - 🧪 **Pilotprojekte:** Starten Sie mit kleineren, überschaubaren Digitalisierungsprojekten
        - 👔 **Leadership:** Sichern Sie aktive Unterstützung der Führungsebene
        """)
    
    # Additional insights based on overall score
    if gesamt_score >= 70:
        st.success("""
        🎉 **Glückwunsch!** Ihr Unternehmen ist bereit für digitale Zwillinge. 
        
        **Empfohlene nächste Schritte:**
        - Kontaktieren Sie spezialisierte Beratungsunternehmen
        - Definieren Sie einen konkreten Use Case für einen Piloten
        - Planen Sie ein Budget für die Umsetzung
        - Identifizieren Sie interne Champions für das Projekt
        """)
    elif gesamt_score >= 40:
        st.info("""
        📈 **Guter Ansatz!** Mit gezielten Verbesserungen können Sie das Potenzial digitaler Zwillinge erschließen.
        
        **Empfohlene nächste Schritte:**
        - Arbeiten Sie zunächst an den identifizierten Schwachstellen
        - Starten Sie mit grundlegenden Digitalisierungsmaßnahmen
        - Bilden Sie ein kleines Digitalisierungsteam
        - Sammeln Sie erste Erfahrungen mit einfacheren Digital-Tools
        """)
    else:
        st.warning("""
        🔧 **Aufbauarbeit nötig:** Legen Sie zunächst die Grundlagen für die Digitalisierung.
        
        **Empfohlene nächste Schritte:**
        - Strukturieren Sie Ihre Datenlandschaft
        - Standardisieren Sie Ihre wichtigsten Prozesse
        - Schulen Sie Ihre Mitarbeiter in digitalen Grundlagen
        - Evaluieren Sie Ihre IT-Infrastruktur
        """)
    
    # Download option
    st.markdown("### 📥 Ergebnisse speichern")
    
    if st.button("📊 Zusammenfassung als Text anzeigen", type="secondary"):
        summary = f"""
# DZ Self-Assessment Ergebnisse

## Gesamtscore: {gesamt_score:.1f}%

## Detaillierte Bewertung:
"""
        for dimension, score in st.session_state.dimension_scores.items():
            summary += f"- {dimension}: {score:.1f}%\n"
        
        summary += f"""
## Stärken:
- {highest_dimension[0]} ({highest_dimension[1]:.1f}%)

## Verbesserungspotenzial:
- {lowest_dimension[0]} ({lowest_dimension[1]:.1f}%)

Erstellt mit dem DZ Self-Assessment Tool
"""
        
        st.text_area("Ihre Zusammenfassung:", summary, height=300)

# Main app logic
def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stRadio > div > div > div > div {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 6px;
        border: 1px solid #e1e5e9;
    }
    .stMultiSelect > div > div > div {
        border-radius: 6px;
    }
    .stProgress > div > div > div {
        background-color: #1f77b4;
    }
    h4 {
        color: #1f77b4;
        border-bottom: 2px solid #e1e5e9;
        padding-bottom: 8px;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Show page header with current step
    current_page = pages[st.session_state.current_page]
    
    # Show current page content
    if st.session_state.current_page == 0:
        show_welcome_page()
    elif st.session_state.current_page == 1:
        show_anwendungspotenzial_page()
    elif st.session_state.current_page == 2:
        show_strategischer_nutzen_page()
    elif st.session_state.current_page == 3:
        show_hemmnisse_page()
    elif st.session_state.current_page == 4:
        show_voraussetzungen_page()
    elif st.session_state.current_page == 5:
        show_results_page()
    
    # Show navigation (except on results page)
    if st.session_state.current_page < len(pages) - 1:
        st.markdown("---")
        show_navigation()
    elif st.session_state.current_page == len(pages) - 1:
        # On results page, offer to restart
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("🔄 Neu starten", type="secondary", use_container_width=True):
                st.session_state.current_page = 0
                st.session_state.answers = {}
                st.session_state.dimension_scores = {}
                st.rerun()
        with col2:
            if st.button("← Zurück zur Übersicht", type="secondary", use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()

if __name__ == "__main__":
    main()