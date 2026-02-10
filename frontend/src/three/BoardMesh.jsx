// frontend/src/three/BoardMesh.jsx
import React, { useMemo, useRef } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import useBoardStore from '../store/boardStore';

const BoardMesh = () => {
  const { boardData } = useBoardStore();
  const meshRef = useRef();

  const geometry = useMemo(() => {
    if (!boardData) return new THREE.BoxGeometry(1, 0.1, 0.3);

    // Dynamic Geometry Generation based on Outline/Rocker
    const geom = new THREE.BufferGeometry();
    const vertices = [];
    const indices = [];

    // 1. Parse Outline Points
    const outline = boardData.outline_points; 
    const length = boardData.dimensions.length;
    
    // Simple mock lofting: Create a top and bottom deck based on outline
    // Real implementation would use Bezier interpolation here
    
    const numPoints = outline.length;
    
    // Top Deck Vertices
    outline.forEach(([x, y], i) => {
        // z represents rocker/thickness. Mocking a simple curve.
        const z = Math.sin((x / length) * Math.PI) * 5.0; 
        vertices.push(x / 10, z / 10, y / 10); // Scale down for viewing
    });

    // Bottom Deck Vertices (Mirrored Y for width, lower Z)
    outline.forEach(([x, y], i) => {
        const z = Math.sin((x / length) * Math.PI) * 5.0 - 0.5; // Thinner
        vertices.push(x / 10, z / 10, y / 10);
    });

    // Create faces (indices)
    // ... Triangulation logic would go here ...

    const verticesFloat32 = new Float32Array(vertices);
    geom.setAttribute('position', new THREE.BufferAttribute(verticesFloat32, 3));
    geom.computeVertexNormals();
    
    return geom;

  }, [boardData]);

  useFrame(() => {
    if (meshRef.current) {
        // Optional: slight rotation or animation
    }
  });

  return (
    <mesh ref={meshRef} geometry={geometry} rotation={[0, 0, 0]}>
      <meshStandardMaterial 
        color="#0077be" 
        roughness={0.4} 
        metalness={0.1}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
};

export default BoardMesh;