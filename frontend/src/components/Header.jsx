import React from 'react'

function Header({ modoTEA, toggleModoTEA, secaoAtiva, setSecaoAtiva }) {
  return (
    <header className="header">
      <div className="container header-content">
        <div className="logo" onClick={() => setSecaoAtiva('home')}>
          <span className="logo-icon">🤝</span>
          <h1>Junta AÍ</h1>
        </div>

        <nav className="nav">
          <button
            className={secaoAtiva === 'home' ? 'nav-link active' : 'nav-link'}
            onClick={() => setSecaoAtiva('home')}
          >
            Início
          </button>
          <button
            className={secaoAtiva === 'questionario' ? 'nav-link active' : 'nav-link'}
            onClick={() => setSecaoAtiva('questionario')}
          >
            Questionário
          </button>
          <button
            className={secaoAtiva === 'estatisticas' ? 'nav-link active' : 'nav-link'}
            onClick={() => setSecaoAtiva('estatisticas')}
          >
            Estatísticas
          </button>
          <button
            className={secaoAtiva === 'apoio' ? 'nav-link active' : 'nav-link'}
            onClick={() => setSecaoAtiva('apoio')}
          >
            Rede de Apoio
          </button>
        </nav>

        <button
          className={`btn-tea ${modoTEA ? 'active' : ''}`}
          onClick={toggleModoTEA}
          title="Modo Confortável para TEA"
        >
          {modoTEA ? '🧩 Modo TEA Ativo' : '🧩 Ativar Modo TEA'}
        </button>
      </div>
    </header>
  )
}

export default Header
