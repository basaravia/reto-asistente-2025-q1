import fitz
import pandas as pd
from tabulate import tabulate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class GetPdfDataframe:
    def __init__(self, ruta: str,cantidad:int=5):
        self.ruta = ruta
        self.cantidad = cantidad
        self.df = self.creacionDataFrame()
        self.df["DEBITO"] = self.df["DEBITO"].str.replace(r'[^\d.]', '', regex=True).astype(float)
        self.df['CREDITO'] = self.df['CREDITO'].str.replace(',', '.').str.replace(' ', '').astype(float)

    def creacionDataFrame(self) -> pd.DataFrame:
        pdf = fitz.open(self.ruta)
        data = []
        for pagina in pdf[1:-1]:
            texto = pagina.get_text("text")
            texto = texto.split("DETALLE DE MOVIMIENTOS")[1]
            texto = texto.split("\n")
            columnas= ["FECHA","OFIC.","N.DOC.","DESCRIPCION","DEBITO","CREDITO","SALDO"]
            texto = [x for x in texto if x != "" and x not in columnas]
            linea = []
            for palabra in texto:
                linea.append(palabra.strip())
                
                if len(linea)==7:
                    data.append(linea)
                    linea = []         
        columns = columnas
        df = pd.DataFrame(data[1:-1], columns=columns)
        df.to_csv("data.csv", index=False,header=True)
        
        return df

    def mayoresGastos(self) -> pd.DataFrame:
        salidas = self.df.groupby('DESCRIPCION')['DEBITO'].sum().reset_index()
        salidas = salidas.sort_values(by='DEBITO', ascending=False)
        return salidas

    def mayoresEntradas(self) -> pd.DataFrame:
        entradas = self.df.groupby('DESCRIPCION')['CREDITO'].sum().reset_index()
        entradas = entradas.sort_values(by='CREDITO', ascending=False)
        return entradas

    def getMayoresVisitas(self) -> pd.DataFrame:
        visitas = self.df.groupby('DESCRIPCION').size().reset_index(name='NUM VISITAS')
        visitas = visitas.sort_values(by='NUM VISITAS', ascending=False)
        return visitas

    def toMarkdown(self,dataframe:pd.DataFrame) -> str:
        return tabulate(dataframe, headers='keys', tablefmt='pipe')

    def getTables(self):
        self.mdGastos=self.toMarkdown(self.mayoresGastos().head(self.cantidad))
        self.mdEntradas=self.toMarkdown(self.mayoresEntradas().head(self.cantidad))
        self.mayoresGastos().to_csv("mayoresGastos.csv", index=False)
        return self.toMarkdown(self.mayoresGastos().head(self.cantidad)), self.toMarkdown(self.mayoresEntradas().head(self.cantidad)),self.toMarkdown(self.getMayoresVisitas().head(self.cantidad))
    
    def resumen(self,modelo:ChatOllama,user_input:str)->str:
        gastos,entradas,visitas = self.getTables()
        inputSystem = """A continuación puedes encontrar la mayor cantidad de gastos de una persona:
        {gastos}
        
        Ahora la mayor cantidad de ingresos de una persona: 
        {entradas}
        
        Ahora puedes ver la mayor cantidad de visitas a un lugar:
        {visitas}
        
        Dame un resumen de los gastos e ingresos de una persona, de una manera corta precisa y rapida, sin dar detalles de las transacciones"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", inputSystem),
            ("user", "Quiero un resumen de los gastos e ingresos de estas tablas además ayudame con lo siguiente: {user_input}")
        ])
        chain = prompt | modelo | StrOutputParser()
        respuesta=chain.invoke({"gastos": gastos, "entradas": entradas, "user_input": user_input,"visitas":visitas}).split("</think>")[1]
        return respuesta

        
        