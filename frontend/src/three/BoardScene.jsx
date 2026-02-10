// frontend/src/three/BoardScene.jsx
import React, { useMemo } from 'react';
import * as THREE from 'three';
import useBoardStore from '../store/boardStore';

const BoardScene = () => {
  const { boardData } = useBoardStore();

  const geometry = useMemo(() => {
    if (!boardData) return null;

    // This logic replaces the Java JOGL rendering.
    // In a real scenario, you might generate the mesh vertices in Python 
    // and send them as an OBJ/STL buffer, or calculate them here in JS 
    // if performance allows.
    
    // Simple placeholder shape based on length/width
    const length = boardData.dimensions.length / 100; // Scale down
    const width = boardData.dimensions.width / 100;
    const box = new THREE.BoxGeometry(length, 0.5, width);
    return box;
  }, [boardData]);

  if (!boardData) return null;

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial color="orange" wireframe={false} />
    </mesh>
  );
};

export default BoardScene;