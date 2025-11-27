import React from 'react'

function InfoCard({ titulo, descricao, icone }) {
  return (
    <div className="info-card">
      <div className="info-icon">{icone}</div>
      <h3>{titulo}</h3>
      <p>{descricao}</p>
    </div>
  )
}

export default InfoCard
