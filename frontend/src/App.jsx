import React, { useState, useEffect } from 'react'
import './styles/App.css'
import Header from './components/Header'
import Hero from './components/Hero'
import Questionario from './components/Questionario'
import Estatisticas from './components/Estatisticas'
import RedeApoio from './components/RedeApoio'
import Footer from './components/Footer'
import InfoCard from './components/InfoCard'

function App() {
  const [modoTEA, setModoTEA] = useState(false)
  const [secaoAtiva, setSecaoAtiva] = useState('home')

  useEffect(() => {
    const teaSalvo = localStorage.getItem('modoTEA')
    if (teaSalvo === 'true') {
      setModoTEA(true)
    }
  }, [])

  const toggleModoTEA = () => {
    const novoModo = !modoTEA
    setModoTEA(novoModo)
    localStorage.setItem('modoTEA', novoModo)
  }

  return (
    <div className={`App ${modoTEA ? 'modo-tea' : ''}`}>
      <Header
        modoTEA={modoTEA}
        toggleModoTEA={toggleModoTEA}
        secaoAtiva={secaoAtiva}
        setSecaoAtiva={setSecaoAtiva}
      />

      <main>
        {secaoAtiva === 'home' && (
          <>
            <Hero setSecaoAtiva={setSecaoAtiva} />

            <section className="info-section">
              <div className="container">
                <h2>O que é violência em relacionamentos?</h2>
                <p className="subtitulo">
                  A violência pode acontecer de diversas formas. Reconhecer os sinais é o primeiro
                  passo para buscar ajuda.
                </p>

                <div className="info-grid">
                  <InfoCard
                    titulo="Violência Física"
                    descricao="Qualquer ato que cause dor ou lesão física: empurrões, tapas, socos, queimaduras, estrangulamento."
                    icone="🤕"
                  />
                  <InfoCard
                    titulo="Violência Psicológica"
                    descricao="Humilhações, insultos, ameaças, isolamento, controle excessivo, ciúmes patológicos, chantagem emocional."
                    icone="😔"
                  />
                  <InfoCard
                    titulo="Violência Sexual"
                    descricao="Forçar relações sexuais, impedir o uso de contraceptivos, expor a doenças propositalmente."
                    icone="🚫"
                  />
                  <InfoCard
                    titulo="Violência Patrimonial"
                    descricao="Controle do dinheiro, destruição de documentos ou bens, impedimento de trabalhar."
                    icone="💰"
                  />
                  <InfoCard
                    titulo="Violência Moral"
                    descricao="Calúnia, difamação, acusações falsas, expor a vida íntima publicamente."
                    icone="🗣️"
                  />
                  <InfoCard
                    titulo="Sinais de Alerta"
                    descricao="Isolamento social, mudanças de comportamento, medo constante, marcas no corpo, desculpas pelo parceiro."
                    icone="⚠️"
                  />
                </div>
              </div>
            </section>

            <section className="cta-section">
              <div className="container">
                <div className="cta-box">
                  <h2>🤝 Você não está sozinha</h2>
                  <p>
                    Se você se identificou com alguma dessas situações, saiba que não é culpa sua e
                    existem pessoas prontas para ajudar. Responder ao questionário pode te ajudar a
                    entender melhor sua situação.
                  </p>
                  <button className="btn btn-large" onClick={() => setSecaoAtiva('questionario')}>
                    Responder Questionário Anônimo
                  </button>
                </div>
              </div>
            </section>
          </>
        )}

        {secaoAtiva === 'questionario' && (
          <Questionario modoTEA={modoTEA} setSecaoAtiva={setSecaoAtiva} />
        )}

        {secaoAtiva === 'estatisticas' && <Estatisticas modoTEA={modoTEA} />}

        {secaoAtiva === 'apoio' && <RedeApoio modoTEA={modoTEA} />}
      </main>

      <Footer />
    </div>
  )
}

export default App
