const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(document.getElementById('3d-view').clientWidth, document.getElementById('3d-view').clientHeight); // Adjust size to fit the container
document.getElementById('3d-view').appendChild(renderer.domElement);

const light = new THREE.PointLight(0xffffff, 2, 500);
light.position.set(0, 0, 0);
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040, 1.2); // Soft white light
scene.add(ambientLight);

function createBody(size, color, position) {
    const geometry = new THREE.SphereGeometry(size, 32, 32);
    const material = new THREE.MeshPhongMaterial({ color: color });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(position.x, position.y, position.z);
    return sphere;
}

function createOrbitPath(radius) {
    const orbitGeometry = new THREE.RingGeometry(radius - 0.2, radius + 0.2, 64);
    const orbitMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
    const orbit = new THREE.Mesh(orbitGeometry, orbitMaterial);
    orbit.rotation.x = Math.PI / 2; // Rotate to align with the x-y plane
    return orbit;
}

const sun = createBody(5, 0xffff00, { x: 0, y: 0, z: 0 });
scene.add(sun);

const celestialBodies = [
    { name: "Mercury", size: 1, color: 0xbebebe, distance: 4 },
    { name: "Venus", size: 1.5, color: 0xffa500, distance: 6 },
    { name: "Earth", size: 1.5, color: 0x0000ff, distance: 8 },
    { name: "Mars", size: 1.2, color: 0xff4500, distance: 10 },
    { name: "Jupiter", size: 3, color: 0xffa07a, distance: 14 },
    { name: "Saturn", size: 2.5, color: 0xf5deb3, distance: 18 },
    { name: "Uranus", size: 2, color: 0x00ffff, distance: 22 },
    { name: "Neptune", size: 2, color: 0x0000ff, distance: 26 },
    { name: "Pluto", size: 0.8, color: 0xdcdcdc, distance: 30 }
];

const bodyMeshes = celestialBodies.map(body => {
    const sphere = createBody(body.size, body.color, { x: body.distance, y: 0, z: 0 });
    const orbit = createOrbitPath(body.distance);
    scene.add(sphere);
    scene.add(orbit);
    return { sphere, distance: body.distance };
});

camera.position.set(0, 60, 90);  // Adjust camera position for better overview
camera.lookAt(0, 0, 0);  // Ensure the camera is looking at the center (Sun)

const animate = function () {
    requestAnimationFrame(animate);

    sun.rotation.y += 0.005;

    bodyMeshes.forEach((bodyMesh, index) => {
        const time = Date.now() * 0.0005 + index;
        bodyMesh.sphere.position.x = bodyMesh.distance * Math.cos(time);
        bodyMesh.sphere.position.z = bodyMesh.distance * Math.sin(time);
        bodyMesh.sphere.rotation.y += 0.01; // Rotate the body itself
    });

    renderer.render(scene, camera);
};

animate();

window.addEventListener('resize', () => {
    const containerWidth = document.getElementById('3d-view').clientWidth;
    const containerHeight = document.getElementById('3d-view').clientHeight;
    camera.aspect = containerWidth / containerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(containerWidth, containerHeight);
});
