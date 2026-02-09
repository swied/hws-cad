// frontend/src/App.jsx
import React, { useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import useBoardStore from './store/boardStore';
import BoardScene from './three/BoardScene';
import Controls from './components/Controls';
import './App.css';

function App() {
  const { fetchBoard } = useBoardStore();

  useEffect(() => {
    fetchBoard();
  }, [fetchBoard]);

  return (
    <div className="app-container" style={{ height: '100vh', display: 'flex' }}>
      <div className="sidebar" style={{ width: '300px', background: '#f4f4f4', padding: '20px' }}>
        <h1>BoardCAD Redux</h1>
        <Controls />
      </div>
      <div className="canvas-container" style={{ flex: 1 }}>
        <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
          <pointLight position={[-10, -10, -10]} />
          
          <BoardScene />
          
          <OrbitControls />
          <gridHelper args={[10, 10]} />
        </Canvas>
      </div>
    </div>
  );
}

export default App;