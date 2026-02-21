import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import GraphExplorer from './pages/GraphExplorer';
import Dashboard from './pages/Dashboard';
import BiomarkerList from './pages/BiomarkerList';
import FoodIndex from './pages/FoodIndex';
import ResearchPapers from './pages/ResearchPapers';
import Recommendations from './pages/Recommendations';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/graph" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="graph" element={<GraphExplorer />} />
          <Route path="biomarkers" element={<BiomarkerList />} />
          <Route path="foods" element={<FoodIndex />} />
          <Route path="papers" element={<ResearchPapers />} />
          <Route path="recommend" element={<Recommendations />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
