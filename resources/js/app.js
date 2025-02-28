import "./bootstrap";
import { createApp } from 'vue';
import ChatComponent from './components/ChatComponent.vue';
import ImageProcessor from "./components/ImageProcessor.vue";

const app = createApp({});
app.component('chat-component', ChatComponent);
console.log('ImageProcessor1', ImageProcessor);
app.component('image-processor', ImageProcessor);
console.log('ImageProcessor2', app);
app.mount('#app');
