import { useState, useEffect } from "react";
import axios from "axios";

import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

function ChatBox({ setLogs }) {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  useEffect(() => {
    if (transcript) {
      let cleaned = transcript;

      // Convert speech variations to ORDxxxx format
      cleaned = cleaned.replace(
        /order\s+(\d+)/gi,
        "ORD$1"
      );

      cleaned = cleaned.replace(
        /ord\s+(\d+)/gi,
        "ORD$1"
      );

      cleaned = cleaned.replace(
        /o\s*r\s*d\s+(\d+)/gi,
        "ORD$1"
      );

      setMessage(cleaned);
    }
  }, [transcript]);

  const startListening = () => {
    resetTranscript();

    SpeechRecognition.startListening({
      continuous: false,
      language: "en-US",
    });
  };

  const sendMessage = async () => {
    if (!message.trim()) {
      return;
    }

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/chat-ai",
        {
          message,
        }
      );

      setResponse(res.data.response);

      const logsRes = await axios.get(
        "http://127.0.0.1:8000/logs"
      );

      setLogs(logsRes.data.logs);
    } catch (error) {
      console.error(error);

      alert(
        "Failed to contact AI agent."
      );
    } finally {
      setLoading(false);
    }
  };

  if (!browserSupportsSpeechRecognition) {
    return (
      <div>
        Browser does not support speech recognition.
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">
        Customer Chat
      </h2>

      <textarea
        className="
          w-full
          border
          rounded-lg
          p-4
          focus:outline-none
          focus:ring-2
          focus:ring-blue-500
        "
        rows="5"
        value={message}
        onChange={(e) =>
          setMessage(e.target.value)
        }
        placeholder="I want a refund for ORD1001"
      />

      <div className="flex gap-3 mt-4">
        <button
          onClick={sendMessage}
          disabled={loading}
          className="
            bg-blue-600
            hover:bg-blue-700
            text-white
            px-5
            py-2
            rounded-lg
            disabled:bg-gray-400
          "
        >
          {loading
            ? "Processing..."
            : "Send"}
        </button>

        <button
          onClick={startListening}
          className="
            bg-green-600
            hover:bg-green-700
            text-white
            px-5
            py-2
            rounded-lg
          "
        >
          🎤 Speak
        </button>
      </div>

      {listening && (
        <div className="mt-3 text-green-600 font-medium">
          🎤 Listening...
        </div>
      )}

      {response && (
        <div
          className="
            mt-6
            p-4
            bg-slate-100
            border
            rounded-lg
          "
        >
          <h3 className="font-bold mb-2">
            Agent Response
          </h3>

          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default ChatBox;