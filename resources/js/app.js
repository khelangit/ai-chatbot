import "./bootstrap";
import { createApp } from 'vue';
import ChatComponent from './components/ChatComponent.vue';
import ImageProcessor from "./components/ImageProcessor.vue";

const app = createApp({
    data() {
        return {
            showImageProcessor: false
        };
    },
    methods: {
        toggleImageProcessor() {
            this.showImageProcessor = !this.showImageProcessor;
        }
    }
});

// Components Register
app.component('chat-component', ChatComponent);
app.component('image-processor', ImageProcessor);

app.mount('#app');

