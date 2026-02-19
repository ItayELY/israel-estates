import React from 'react';
import PropertyCard from './PropertyCard';

export default function PropertyGrid({ properties, loading }) {
    if (loading) {
        return (
            <div className="container grid-container">
                <div className="loading-state">
                    <div className="spinner"></div>
                    <p>Finding perfect homes...</p>
                </div>
            </div>
        );
    }

    if (!properties || properties.length === 0) {
        return (
            <div className="container grid-container">
                <div className="empty-state glass-panel">
                    <h2>No properties found</h2>
                    <p>Try adjusting your search filters to find what you're looking for.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container grid-container">
            <div className="grid-header">
                <h2>Featured Properties</h2>
                <p className="results-count">{properties.length} results</p>
            </div>

            <div className="properties-grid">
                {properties.map((property, index) => (
                    <div key={property.id} style={{ animationDelay: `${index * 50}ms` }}>
                        <PropertyCard property={property} />
                    </div>
                ))}
            </div>

            <style>{`
        .grid-container {
          padding-top: 4rem;
          padding-bottom: 4rem;
        }

        .grid-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-end;
          margin-bottom: 2rem;
        }

        .grid-header h2 {
          font-size: 2rem;
        }

        .results-count {
          color: var(--text-secondary);
          font-weight: 500;
          font-size: 1.1rem;
        }

        .properties-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 2rem;
        }

        .loading-state, .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 5rem 2rem;
          text-align: center;
        }

        .empty-state {
          background: white;
        }

        .empty-state h2 {
          font-size: 1.5rem;
          margin-bottom: 0.5rem;
        }

        .empty-state p {
          color: var(--text-secondary);
        }

        .spinner {
          width: 40px;
          height: 40px;
          border: 3px solid var(--primary-light);
          border-top-color: var(--primary);
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 1rem;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
        </div>
    );
}
