import { useEffect, useRef, useState } from "react";

export default function Camera() {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const detectionsRef = useRef<HTMLDivElement>(null);
    const [streaming, setStreaming] = useState<boolean>(false);
    const [isVideoMode, setIsVideoMode] = useState(true); // true = video, false = image


    const socketRef = useRef<WebSocket | null>(null);

    // Initialize canvas context and dimensions
    useEffect(() => {
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (video && canvas) {
            video.addEventListener('loadedmetadata', () => {
                const ctx = canvas.getContext('2d');
                if (ctx) {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    console.log('Canvas dimensions updated:', canvas.width, canvas.height);
                    drawBoundingBox(ctx, 50, 50, 200, 200); // Test with hardcoded values
                }
            });
        }
    }, []);

    // Start streaming
    const startStreaming = async () => {
        const video = videoRef.current;
        const canvas = canvasRef.current;

        if (!video || !canvas) return;

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.play();

            // Set canvas dimensions to match video
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            // Connect to WebSocket
            socketRef.current = new WebSocket('ws://localhost:8000/ws/detect');

            socketRef.current.onopen = () => {
                console.log('WebSocket connection established');
                setStreaming(true);
                console.log('set streaming', streaming)
                sendFrames(true);
            };

            socketRef.current.onmessage = (event) => {
                console.log('streaming>>>>>>>')
                const data = JSON.parse(event.data);
                if (data.detections && detectionsRef.current) {
                    const ctx = canvas.getContext('2d');
                    if (ctx) {
                        // Clear the canvas and draw the current video frame
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                        // Draw bounding boxes for detected objects
                        data.detections.forEach((obj: any) => {
                            drawBoundingBox(ctx, obj.box.x1, obj.box.y1, obj.box.x2, obj.box.y2);
                        });

                        // Display detection labels
                        detectionsRef.current.innerHTML = data.detections
                            .map(
                                (obj: any) =>
                                    `<p>${obj.label}: ${obj.confidence.toFixed(2)}</p>`
                            )
                            .join('');
                    }
                }
            };

            socketRef.current.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            socketRef.current.onclose = () => {
                console.log('WebSocket connection closed');
                setStreaming(false);
            };
        } catch (error) {
            console.error('Error accessing camera:', error);
        }
    };

    // Stop streaming
    const stopStreaming = () => {
        setStreaming(false);
        if (socketRef.current) {
            socketRef.current.close();
        }
        const video = videoRef.current;
        if (video && video.srcObject) {
            const stream = video.srcObject as MediaStream;
            stream.getTracks().forEach((track) => track.stop());
        }
    };

    const sendFrames = (isStream: boolean) => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const socket = socketRef.current;

        // Check if streaming is active and all required elements are available

        if (!isStream || !video || !canvas || !socket || socket.readyState !== WebSocket.OPEN) {
            console.log("it prevent here")
            return;
        }

        const ctx = canvas.getContext('2d');
        if (ctx) {
            // Capture frame from video
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const frame = canvas.toDataURL('image/jpeg', 0.5); // Convert to base64
            console.log(frame)
            // Send frame to server
            socket.send(frame);

            // Continuously call sendFrames to maintain the stream
            requestAnimationFrame(sendFrames);
        }
    };

    // Draw bounding box on the canvas
    const drawBoundingBox = (
        ctx: CanvasRenderingContext2D,
        x1: number,
        y1: number,
        x2: number,
        y2: number
    ) => {
        ctx.beginPath();
        ctx.rect(x1, y1, x2 - x1, y2 - y1); // Draw rectangle
        ctx.strokeStyle = 'red'; // Box color
        ctx.lineWidth = 2; // Box thickness
        ctx.stroke();
    };

    const toggleMode = () => {
        setIsVideoMode((prev) => !prev);
    };

    return (
        <div className="border-5 border-indigo-500 ">
            <div className="">
                <video ref={videoRef} width="1000" height="480" muted autoPlay />
                <canvas ref={canvasRef} width="1000" height="480" style={{ display: 'none' }} />
            </div>

            <div className="flex justify-between bg-gray-500 px-4">
                <div className="mt-4 flex items-center space-x-2">
                    <button
                        onClick={toggleMode}
                        className={`w-18 h-6 flex items-center rounded-full px-1 py- ${isVideoMode ? 'bg-blue-500' : 'bg-gray-300'
                            }`}
                    >
                        <span className={`fixed  ${isVideoMode ? '' : 'translate-x-6'}`}>{isVideoMode ? `video` : `image`}</span>
                        <div
                            className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform ${isVideoMode ? 'translate-x-12' : 'translate-x-0'
                                }`}
                        />
                    </button>

                </div>
                {
                    isVideoMode ? (<div className="flex justify-center gap-4 py-4">
                        <button className="bg-green-500 rounded-xl p-2 font-bold text-white" onClick={startStreaming} disabled={streaming}>
                            Recording
                        </button>
                        <button className="bg-red-500 rounded-xl p-2 font-bold text-white" onClick={stopStreaming} disabled={!streaming}>
                            Stop recording
                        </button>
                    </div>) : <div className="py-4">
                        <button className="bg-green-500 rounded-xl p-2 font-bold text-white" onClick={startStreaming} disabled={streaming}>
                            upload
                        </button>
                    </div>
                }

            </div>



        </div>

    )
}