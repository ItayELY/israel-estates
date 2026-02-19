import { useState, useCallback, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroSearch from './components/HeroSearch';
import PropertyGrid from './components/PropertyGrid';
import './index.css';

function App() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    city: '',
    type: '',
    max_budget: ''
  });

  const fetchProperties = useCallback(async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams();
      if (filters.city) queryParams.append('city', filters.city);
      if (filters.type) queryParams.append('type', filters.type);
      if (filters.max_budget) queryParams.append('max_budget', filters.max_budget);

      const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000';
      const response = await fetch(`${apiUrl}/api/properties?${queryParams.toString()}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setProperties(data);
    } catch (error) {
      console.error('Error fetching properties:', error);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Initial fetch
  useEffect(() => {
    fetchProperties();
  }, []); // Only fetch once on mount

  const handleSearch = () => {
    fetchProperties();
  };

  return (
    <div className="app-wrapper">
      <Navbar />
      <main>
        <HeroSearch
          onSearch={handleSearch}
          filters={filters}
          setFilters={setFilters}
        />
        <PropertyGrid
          properties={properties}
          loading={loading}
        />
      </main>

      <footer className="footer">
        <div className="container">
          <p>&copy; {new Date().getFullYear()} IsraelEstates. All rights reserved.</p>
        </div>
      </footer>

      <style>{`
        .app-wrapper {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        main {
          flex: 1;
        }

        .footer {
          background-color: var(--secondary);
          color: white;
          padding: 3rem 0;
          text-align: center;
          margin-top: auto;
        }

        .footer p {
          color: var(--text-muted);
        }
      `}</style>
    </div>
  );
}

export default App;
