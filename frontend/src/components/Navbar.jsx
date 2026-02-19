import React from 'react';
import { Building2, UserCircle } from 'lucide-react';

export default function Navbar() {
    return (
        <nav className="navbar">
            <div className="container nav-container">
                <a href="/" className="logo">
                    <Building2 size={24} className="logo-icon" />
                    <span>Israel<span className="logo-highlight">Estates</span></span>
                </a>

                <div className="nav-links">
                    <a href="#" className="nav-link">Rentals</a>
                    <a href="#" className="nav-link">For Sale</a>
                    <a href="#" className="nav-link">Agents</a>
                </div>

                <div className="nav-actions">
                    <button className="btn btn-outline nav-btn">
                        <UserCircle size={18} />
                        Sign In
                    </button>
                </div>
            </div>
            <style>{`
        .navbar {
          background-color: var(--surface);
          border-bottom: 1px solid var(--border);
          position: sticky;
          top: 0;
          z-index: 100;
          box-shadow: var(--shadow-sm);
        }

        .nav-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 80px;
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-family: var(--font-heading);
          font-weight: 800;
          font-size: 1.5rem;
          color: var(--secondary);
        }

        .logo-icon {
          color: var(--primary);
        }

        .logo-highlight {
          color: var(--primary);
        }

        .nav-links {
          display: flex;
          gap: 2rem;
        }

        .nav-link {
          font-weight: 500;
          color: var(--text-secondary);
          transition: color var(--transition-fast);
        }

        .nav-link:hover {
          color: var(--primary);
        }

        .nav-btn {
          border-radius: 9999px;
          padding: 0.5rem 1.25rem;
        }

        @media (max-width: 768px) {
          .nav-links {
            display: none;
          }
        }
      `}</style>
        </nav>
    );
}
