import { useEffect } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export default function App() {
  useEffect(() => {
    const scene = new THREE.Scene();
    const cubeGeometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
    const cubeMaterial = new THREE.MeshBasicMaterial({ color: 'red' });
    const cubeMesh = new THREE.Mesh(cubeGeometry, cubeMaterial);
    scene.add(cubeMesh);

    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      3.9,
      6
    );

    const aspectRatio = window.innerWidth / window.innerHeight;
    const orthCamera = new THREE.OrthographicCamera(
      -0.5 * aspectRatio,
      0.5 * aspectRatio,
      -0.5,
      0.5,
      0.1,
      1000
    );
    orthCamera.position.z = 5;
    camera.position.z = 5;

    scene.add(orthCamera);

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    const canvasContainer = document.getElementById('canvas-container');
    canvasContainer?.appendChild(renderer.domElement);

    const orbit = new OrbitControls(orthCamera, renderer.domElement);
    orbit.autoRotate = true;
    orbit.autoRotateSpeed = 0.5;
    function animate() {
      requestAnimationFrame(animate);
      // cubeMesh.rotation.x += 0.01;
      // cubeMesh.rotation.y += 0.01;
      orbit.update();
      renderer.render(scene, orthCamera);
    }
    animate();
  }, []);

  return <div id="canvas-container" />;
}
