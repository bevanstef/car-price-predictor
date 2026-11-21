import React, { useState } from 'react'
import SelectField from './components/SelectField'

// Exact brand-to-model hierarchy matching the training dataset
const BRAND_MODELS = {
  Toyota: ['Aqua', 'Prius', 'Corolla', 'Vitz', 'Axio'],
  Suzuki: ['Alto', 'Wagon R', 'Swift', 'Every'],
  Honda: ['Fit', 'Vezel', 'Civic', 'Grace'],
  Nissan: ['Leaf', 'Sunny', 'X-Trail', 'March'],
  Mitsubishi: ['Montero', 'Lancer', 'Mirage'],
  Micro: ['Panda', 'Geely'],
  Kia: ['Picanto', 'Rio', 'Sportage'],
  Perodua: ['Axia', 'Bezza'],
}

const FUELS = ['Petrol', 'Diesel', 'Hybrid', 'Electric']
const TRANSMISSIONS = ['Automatic', 'Manual']
const ENGINE_CAPACITIES = [660, 800, 1000, 1300, 1500, 1800, 2000]

export default function App() {
  const [formData, setFormData] = useState({
    brand: 'Toyota',
    model: 'Aqua',
    year: 2018,
    mileage_km: 50000,
    fuel: 'Hybrid',
    transmission: 'Automatic',
    engine_cc: 1500,
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Fields that must be converted to numbers
  const NUMERIC_FIELDS = ['year', 'mileage_km', 'engine_cc']

  const handleBrandChange = (e) => {
    const newBrand = e.target.value
    const defaultModel = BRAND_MODELS[newBrand][0]
    setFormData((prev) => ({
      ...prev,
      brand: newBrand,
      model: defaultModel,
    }))
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: NUMERIC_FIELDS.includes(name) ? Number(value) : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`)
      }

      const data = await response.json()
      setPrediction(data.price_lkr)
    } catch (err) {
      setError('Unable to get prediction. Ensure backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Used Car Price Predictor (Sri Lanka)</h1>
      <p className="subtitle">Enter vehicle details to estimate market price in LKR</p>

      <form onSubmit={handleSubmit} className="card">
        {/* Brand Dropdown */}
        <div className="form-group">
          <label htmlFor="brand">Brand</label>
          <select id="brand" name="brand" value={formData.brand} onChange={handleBrandChange}>
            {Object.keys(BRAND_MODELS).map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </div>

        {/* Model Dropdown (Dependent on Brand) */}
        <SelectField
          id="model"
          name="model"
          label="Model"
          value={formData.model}
          options={BRAND_MODELS[formData.brand]}
          onChange={handleChange}
        />

        {/* Year Input */}
        <div className="form-group">
          <label htmlFor="year">Year (2005 - 2024)</label>
          <input
            id="year"
            name="year"
            type="number"
            min="2005"
            max="2024"
            value={formData.year}
            onChange={handleChange}
            required
          />
        </div>

        {/* Mileage Input */}
        <div className="form-group">
          <label htmlFor="mileage_km">Mileage (km)</label>
          <input
            id="mileage_km"
            name="mileage_km"
            type="number"
            min="0"
            max="400000"
            value={formData.mileage_km}
            onChange={handleChange}
            required
          />
        </div>

        {/* Fuel Dropdown */}
        <SelectField
          id="fuel"
          name="fuel"
          label="Fuel Type"
          value={formData.fuel}
          options={FUELS}
          onChange={handleChange}
        />

        {/* Transmission Dropdown */}
        <SelectField
          id="transmission"
          name="transmission"
          label="Transmission"
          value={formData.transmission}
          options={TRANSMISSIONS}
          onChange={handleChange}
        />

        {/* Engine Capacity Dropdown */}
        <SelectField
          id="engine_cc"
          name="engine_cc"
          label="Engine Capacity (cc)"
          value={formData.engine_cc}
          options={ENGINE_CAPACITIES}
          onChange={handleChange}
        />

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Calculating...' : 'Predict Price'}
        </button>
      </form>

      {error && <div className="banner error">{error}</div>}

      {prediction && (
        <div className="banner success">
          <h3>Estimated Price:</h3>
          <p className="price">Rs. {prediction.toLocaleString('en-LK')}</p>
        </div>
      )}
    </div>
  )
}
