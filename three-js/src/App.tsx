import * as THREE from "three";
import { useEffect } from "react";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

export default function App() {
  useEffect(() => {
    const canvasContainer = document.getElementById("canvas-container");
    if (!canvasContainer) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.set(0, 0, 5);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
    });
    canvasContainer.appendChild(renderer.domElement);
    renderer.setSize(window.innerWidth, window.innerHeight);
    const maxPixelRatio = Math.min(window.devicePixelRatio, 2);
    renderer.setPixelRatio(maxPixelRatio);
    const controls = new OrbitControls(camera, renderer.domElement);

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const materials = [
      new THREE.MeshBasicMaterial({ color: 0xff0000}), // right
      new THREE.MeshBasicMaterial({ color: 0x00ff00 }), // left
      new THREE.MeshBasicMaterial({ color: 0x0000ff }), // top
      new THREE.MeshBasicMaterial({ color: 0xffff00 }), // bottom
      new THREE.MeshBasicMaterial({ color: 0xff00ff  }), // front
      new THREE.MeshBasicMaterial({ color: 0x00ffff }), // back
    ];


    const mesh = new THREE.Mesh(geometry, materials);
    mesh.position.set(0, 0, 0);
    mesh.rotation.reorder("XYZ");
    // mesh.rotation.y = THREE.MathUtils.degToRad(60);
    const mesh2 = new THREE.Mesh(geometry, materials);
    mesh2.position.set(0, 0, 2);
    const mesh3 = new THREE.Mesh(geometry, materials);
    mesh3.position.set(0, 0, -2);

    const group = new THREE.Group();
    group.position.set(0, 0, 0);
    group.add(mesh);
    group.add(mesh2);
    group.add(mesh3);

    const axisHelper = new THREE.AxesHelper(5);
    scene.add(axisHelper);
    scene.add(group);
    console.log(
      "mesh distance from camera",
      mesh.position.distanceTo(camera.position)
    );

    window.addEventListener("resize", () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    function animate() {
      window.requestAnimationFrame(animate);
      mesh.rotation.x = Math.PI / 3

      controls.update();
      renderer.render(scene, camera);
    }
    animate();
  }, []);
  return <div id="canvas-container" />;
}
