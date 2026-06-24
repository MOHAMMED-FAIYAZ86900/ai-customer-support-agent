import { useState } from "react";

import ChatBox from "./components/ChatBox";
import LogsPanel from "./components/LogsPanel";

function App() {

  const [logs, setLogs] = useState([]);

  return (

    <div className="min-h-screen bg-slate-100 p-8">

      <h1 className="text-4xl font-bold mb-8">
        AI Customer Support Agent
      </h1>

      <div className="grid grid-cols-2 gap-6">

        <div
          className="
            bg-white
            p-6
            rounded-xl
            shadow
          "
        >
          <ChatBox
            setLogs={setLogs}
          />
        </div>

        <div
          className="
            bg-white
            p-6
            rounded-xl
            shadow
          "
        >
          <LogsPanel
            logs={logs}
          />
        </div>

      </div>

    </div>

  );
}

export default App;