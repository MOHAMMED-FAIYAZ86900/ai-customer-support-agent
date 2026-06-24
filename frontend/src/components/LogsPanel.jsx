function LogsPanel({ logs }) {

  const getColor = (status) => {

    if (
      status === "passed" ||
      status === "approved"
    ) {
      return "text-green-600";
    }

    if (
      status === "failed" ||
      status === "denied"
    ) {
      return "text-red-600";
    }

    return "text-yellow-600";
  };

  const finalLog =
    logs.find(
      (log) =>
        log.step === "Final Decision"
    );

  return (
    <div>

      <h2 className="text-xl font-bold mb-4">
        Agent Reasoning Logs
      </h2>

      {finalLog && (

        <div
          className={`mb-4 p-4 rounded-lg font-bold ${
            finalLog.status === "approved"
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {finalLog.status === "approved"
            ? "🟢 Refund Approved"
            : "🔴 Refund Denied"}
        </div>

      )}

      <div className="space-y-3">

        {logs.map((log, index) => (

          <div
            key={index}
            className="
              bg-slate-50
              border
              rounded-lg
              p-3
            "
          >

            <div className="flex justify-between">

              <span>
                {log.step}
              </span>

              <span
                className={getColor(
                  log.status
                )}
              >
                {log.status}
              </span>

            </div>

            <div className="text-xs text-gray-500 mt-1">
              {log.time}
            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

export default LogsPanel;