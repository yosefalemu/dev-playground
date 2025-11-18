import * as THREE from 'three';

export default function App() {
  console.log('THREE MODULE', THREE);
  const scene = new THREE.Scene();
  console.log('SCENE', scene);

  const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
  const cubeMaterial = new THREE.MeshBasicMaterial({ color: 'red' });

  const cubeMesh = new THREE.Mesh(cubeGeometry, cubeMaterial);

  scene.add(cubeMesh);
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );

  camera.position.z = 5;

  scene.add(camera);

  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  const canvasContainer = document.getElementById('canvas-container');
  console.log('CANVAS CONTAINER', canvasContainer);
  canvasContainer?.appendChild(renderer.domElement);

  function animate() {
    window.requestAnimationFrame(animate);
    cubeMesh.rotation.x += 0.01;
    cubeMesh.rotation.y += 0.01;
    renderer.render(scene, camera);
  }
  animate();

  return <div id="canvas-container" />;
}
