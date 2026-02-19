import React from 'react';
import { MapPin, Home, DollarSign, Search } from 'lucide-react';

export default function HeroSearch({ 
  onSearch, 
  filters, 
  setFilters 
}) {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch();
  };

  return (
    <div className="hero-container">
      <div className="hero-content animate-fade-in">
        <h1 className="hero-title">
          Find Your Dream Home in Israel
        </h1>
        <p className="hero-subtitle">
          Premium property search for Tel Aviv and Holon.
        </p>

        <form className="search-form glass-panel" onSubmit={handleSearch}>
          <div className="search-inputs-wrapper">
            
            {/* Property Type */}
            <div className="search-input-group">
              <label><Home size={14} style={{display:'inline', marginRight:'4px'}}/> Type</label>
              <select name="type" value={filters.type} onChange={handleChange}>
                <option value="">Any</option>
                <option value="Rent">Rent</option>
                <option value="Buy">Buy</option>
              </select>
            </div>
            
            <div className="search-divider"></div>
            
            {/* City */}
            <div className="search-input-group">
              <label><MapPin size={14} style={{display:'inline', marginRight:'4px'}}/> Location</label>
              <select name="city" value={filters.city} onChange={handleChange}>
                <option value="">Any City</option>
                <option value="Tel Aviv">Tel Aviv</option>
                <option value="Holon">Holon</option>
              </select>
            </div>

            <div className="search-divider"></div>
            
            {/* Budget */}
            <div className="search-input-group">
              <label><DollarSign size={14} style={{display:'inline', marginRight:'4px'}}/> Max Budget (ILS)</label>
              <input 
                type="number" 
                name="max_budget" 
                placeholder="No Limit" 
                value={filters.max_budget}
                onChange={handleChange}
                min="0"
                step="1000"
              />
            </div>

          </div>

          <button type="submit" className="btn btn-primary search-btn">
            <Search size={18} /> Search
          </button>
        </form>
      </div>
      <style>{`
        .hero-container {
          position: relative;
          padding: 6rem 1.5rem;
          min-height: 50vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(to right bottom, var(--primary-light), white);
          overflow: hidden;
        }

        .hero-container::before {
          content: '';
          position: absolute;
          top: -50%; left: -50%; width: 200%; height: 200%;
          background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 50%);
          z-index: 0;
        }

        .hero-content {
          position: relative;
          z-index: 1;
          width: 100%;
          max-width: 900px;
          text-align: center;
        }

        .hero-title {
          font-size: clamp(2.5rem, 5vw, 4rem);
          margin-bottom: 1rem;
          background: linear-gradient(to right, var(--secondary), var(--primary));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
          font-size: 1.25rem;
          color: var(--text-secondary);
          margin-bottom: 3rem;
        }

        .search-form {
          display: flex;
          align-items: center;
          padding: 1rem 1.5rem;
          gap: 1.5rem;
          background: rgba(255, 255, 255, 0.85);
        }

        .search-inputs-wrapper {
          display: flex;
          flex: 1;
          align-items: center;
        }

        .search-btn {
          padding: 1rem 2.25rem;
          font-size: 1.1rem;
          border-radius: 12px;
        }

        @media (max-width: 768px) {
          .search-form {
            flex-direction: column;
            padding: 1.5rem;
          }
          .search-inputs-wrapper {
            flex-direction: column;
            width: 100%;
          }
          .search-input-group label {
            margin-bottom: 0.5rem;
          }
          .search-btn {
            width: 100%;
            margin-top: 1rem;
          }
        }
      `}</style>
    </div>
  );
}
