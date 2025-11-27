import React from 'react'

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>🤝 Junta AÍ</h3>
            <p>
              Plataforma de conscientização e apoio para pessoas em situação de violência em
              relacionamentos.
            </p>
          </div>

          <div className="footer-section">
            <h4>Contatos de Emergência</h4>
            <ul>
              <li>
                📞 <a href="tel:180">180 - Central da Mulher</a>
              </li>
              <li>
                📞 <a href="tel:190">190 - Polícia Militar</a>
              </li>
              <li>
                📞 <a href="tel:188">188 - CVV (Apoio Emocional)</a>
              </li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Recursos</h4>
            <ul>
              <li>Lei Maria da Penha</li>
              <li>Defensoria Pública</li>
              <li>Delegacia da Mulher</li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>
            &copy; 2025 Junta AÍ. Este projeto visa conscientizar e apoiar pessoas em situação de
            violência.
          </p>
          <p className="footer-disclaimer">🔒 Seus dados são completamente anônimos e seguros.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
