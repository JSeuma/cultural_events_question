import streamlit as st
import sys
sys.path.append('sqlchain_cultura.py')
import sqlchain_cultura as codi

def run():
    st.title("La cultura ens alimenta")
    st.subheader("Buscador cultural")
    st.markdown('#### Introdueix la teva pregunta sobre la oferta cultural de Catalunya')
    
    query = st.text_input('Quina és la teva pregunta?')
    
    # Execute the function and display the result only if a query is provided
    if query:  # Checks if 'query' is not empty
        result = codi.cultura_es_vida(query)
        st.markdown(f"<p style='color: green; font-size: 24px;'>{result}</p>", unsafe_allow_html=True)
    
    st.markdown(":smile:")
    st.markdown("Marca el quadrat si t'ha agradat l'eina")
    st.button('Aquí')
    st.balloons()
    
    
    if 'message' not in st.session_state:
        st.session_state.message = []

if __name__ == "__main__":
    run()
