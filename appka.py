import streamlit as st
import pickle
from datetime import datetime
startTime = datetime.now()
#import bibliotek

filename = "model.sv"
model = pickle.load(open(filename,'rb'))
#otworzenie wytrenowanego model

Sex_d = {0:"kobieta", 1:"mężczyzna"}
ChestPainType_d = {0:"bezobjawowy", 1:"dławica atypowa", 2:"ból niedławicowy", 3:"typowa dławica" }
RestingECG_d = {0:"przerost lewej komory", 1:"normalny", 2:"z nieprawidłowym załamkiem"}
ExerciseAngina_d = {0:"Nie", 1:"Tak"}
ST_Slope_d = {0:"opadające", 1:"płaskie", 2:"wznoszące"}

#odkodowanie zmiennych i dodanie etykiet z powrotem

def main():

	st.set_page_config(page_title="Sprawdź zdrowie twojego serca!")
	overview = st.container()
	left, right = st.columns(2)
	prediction = st.container()

	st.image("https://static.vecteezy.com/system/resources/previews/009/341/714/original/hand-draw-heart-icon-love-sign-design-free-png.png")

	with overview:
		st.title("Sprawdź zdrowie twojego serca!")

	with left:
		Sex_radio = st.radio( "Płeć", list(Sex_d.keys()), format_func=lambda x : Sex_d[x] )
		ChestPainType_radio = st.radio( "Typ bólu klatki piersiowej", list(ChestPainType_d.keys()), index=2, format_func= lambda x: ChestPainType_d[x] )
		RestingECG_radio = st.radio( "EKG spoczynkowe", list(RestingECG_d.keys()), format_func=lambda x : RestingECG_d[x] )
		ExerciseAngina_radio = st.radio( "Czy ćwiczysz", list(ExerciseAngina_d.keys()), format_func=lambda x : ExerciseAngina_d[x] )
		ST_Slope_radio = st.radio( "Nachylenie w szczytowym momencie ćwiczeń", list(ST_Slope_d.keys()), format_func=lambda x : ST_Slope_d[x] )

	with right:
		Age_slider = st.slider("Wiek", value=1, min_value=28, max_value=77)
		RestingBP_slider = st.slider("Spoczynkowe ciśnienie krwi", min_value=0, max_value=200)
		Cholesterol_slider = st.slider("Cholesterol", min_value=0, max_value=603)
		FastingBS_slider = st.slider("Poziom cukruw we krwi", min_value=0, max_value=1)
		MaxHR_slider = st.slider("Maksymalne tętno", min_value=60, max_value=202)
		#Oldpeak_slider = st.slider("Oldpeak", min_value=-2, max_value=7)


	data = [[Sex_radio, ChestPainType_radio,  RestingECG_radio, ExerciseAngina_radio, ST_Slope_radio, Age_slider, RestingBP_slider,Cholesterol_slider, FastingBS_slider, MaxHR_slider]]
	survival = model.predict(data)
	s_confidence = model.predict_proba(data)

	with prediction:
		st.subheader("Czy masz chorobę serca?")
		st.subheader(("Tak, skonsultuj się z lekarzem" if survival[0] == 1 else "Nie, możesz spać spokojnie"))
		st.write("Pewność predykcji {0:.2f} %".format(s_confidence[0][survival][0] * 100))

if __name__ == "__main__":
    main()