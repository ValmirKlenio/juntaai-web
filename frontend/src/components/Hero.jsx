import React from 'react'
import imageHome from '../assets/image_home.png'

function Hero({ setSecaoAtiva }) {
  return (
    <section className="hero">
      <div className="container hero-content">
        <div className="hero-text">
          <h1 className="hero-title">Você não está sozinha</h1>
          <p className="hero-subtitle">
            Um espaço seguro e anônimo para entender sua situação e encontrar apoio. Aqui você pode
            avaliar seu relacionamento sem julgamentos.
          </p>
          <div className="hero-buttons">
            <button
              className="btn btn-primary btn-large"
              onClick={() => setSecaoAtiva('questionario')}
            >
              Fazer Questionário Anônimo
            </button>
            <button className="btn btn-secondary btn-large" onClick={() => setSecaoAtiva('apoio')}>
              Buscar Ajuda Agora
            </button>
          </div>
          <div className="hero-alert">
            <span className="alert-icon">🔒</span>
            <p>
              <strong>100% Anônimo e Seguro.</strong> Suas respostas não são identificadas e ajudam
              a gerar dados para pesquisa.
            </p>
          </div>
        </div>

        <div className="hero-image">
          <div className="image-placeholder">
            <img
              src={imageHome}
              alt="Ilustração de acolhimento e escuta"
              className="hero-illustration"
            />
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero
