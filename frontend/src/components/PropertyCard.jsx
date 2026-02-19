import React from 'react';
import { MapPin, Bed, Bath, Square } from 'lucide-react';

export default function PropertyCard({ property }) {
    // Format price with commas
    const formatPrice = (price) => {
        return new Intl.NumberFormat('he-IL', {
            style: 'currency',
            currency: 'ILS',
            maximumFractionDigits: 0
        }).format(price);
    };

    return (
        <div className="property-card glass-panel animate-fade-in">
            <div className="card-image-wrapper">
                <img src={property.image_url} alt={property.title} className="card-image" />
                <div className="card-badges">
                    <span className={`badge ${property.type === 'Rent' ? 'badge-rent' : 'badge-buy'}`}>
                        For {property.type}
                    </span>
                    <span className="badge badge-city">
                        <MapPin size={12} style={{ marginRight: '4px' }} />
                        {property.city}
                    </span>
                </div>
                <div className="card-price">
                    {formatPrice(property.price)}
                    {property.type === 'Rent' && <span className="price-period">/mo</span>}
                </div>
            </div>

            <div className="card-content">
                <h3 className="card-title">{property.title}</h3>
                <p className="card-desc">{property.description}</p>

                <div className="card-meta">
                    <div className="meta-item">
                        <Bed size={16} />
                        <span>3 Beds</span>
                    </div>
                    <div className="meta-item">
                        <Bath size={16} />
                        <span>2 Baths</span>
                    </div>
                    <div className="meta-item">
                        <Square size={16} />
                        <span>120 m²</span>
                    </div>
                </div>
            </div>

            <div className="card-footer">
                <button className="btn btn-outline btn-block" style={{ borderRadius: '8px' }}>
                    View Details
                </button>
            </div>

            <style>{`
        .property-card {
          display: flex;
          flex-direction: column;
          overflow: hidden;
          transition: transform var(--transition-normal), box-shadow var(--transition-normal);
          background: white;
          border-radius: 20px;
        }

        .property-card:hover {
          transform: translateY(-5px);
          box-shadow: var(--shadow-xl);
        }

        .card-image-wrapper {
          position: relative;
          height: 240px;
          overflow: hidden;
        }

        .card-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform var(--transition-slow);
        }

        .property-card:hover .card-image {
          transform: scale(1.05);
        }

        .card-badges {
          position: absolute;
          top: 1rem;
          left: 1rem;
          display: flex;
          gap: 0.5rem;
        }

        .badge {
          display: flex;
          align-items: center;
          padding: 0.35rem 0.75rem;
          border-radius: 9999px;
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          backdrop-filter: blur(8px);
        }

        .badge-rent {
          background: rgba(59, 130, 246, 0.9);
          color: white;
        }

        .badge-buy {
          background: rgba(245, 158, 11, 0.9);
          color: white;
        }

        .badge-city {
          background: rgba(15, 23, 42, 0.8);
          color: white;
        }

        .card-price {
          position: absolute;
          bottom: 1rem;
          right: 1rem;
          background: rgba(255, 255, 255, 0.95);
          color: var(--secondary);
          padding: 0.5rem 1rem;
          border-radius: 12px;
          font-family: var(--font-heading);
          font-weight: 700;
          font-size: 1.25rem;
          box-shadow: var(--shadow-md);
        }

        .price-period {
          font-size: 0.875rem;
          color: var(--text-secondary);
          font-weight: 500;
        }

        .card-content {
          padding: 1.5rem;
          flex: 1;
        }

        .card-title {
          font-size: 1.25rem;
          margin-bottom: 0.5rem;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .card-desc {
          color: var(--text-secondary);
          font-size: 0.95rem;
          margin-bottom: 1.5rem;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .card-meta {
          display: flex;
          justify-content: space-between;
          padding-top: 1rem;
          border-top: 1px solid var(--border);
        }

        .meta-item {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          color: var(--text-muted);
          font-size: 0.875rem;
          font-weight: 500;
        }

        .card-footer {
          padding: 0 1.5rem 1.5rem;
        }
      `}</style>
        </div>
    );
}
