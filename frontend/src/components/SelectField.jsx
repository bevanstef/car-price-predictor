import React from 'react'

/**
 * Reusable Select dropdown component
 */
export default function SelectField({ id, name, label, value, options, onChange }) {
  return (
    <div className="form-group">
      <label htmlFor={id}>{label}</label>
      <select id={id} name={name} value={value} onChange={onChange}>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  )
}
