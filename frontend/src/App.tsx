import { useEffect, useState } from "react";

type ConnectionState = "checking" | "connected" | "failed";

function App() {
  const [connectionState, setConnectionState] = useState<ConnectionState>("checking");

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch("/api/health");

        if (!response.ok) {
          throw new Error(`Health check failed with status ${response.status}`);
        }

        const body: unknown = await response.json();

        if (
          typeof body !== "object" ||
          body === null ||
          !("status" in body) ||
          body.status !== "ok"
        ) {
          throw new Error("Unexpected health response");
        }

        setConnectionState("connected");
      } catch {
        setConnectionState("failed");
      }
    };

    void checkBackend();
  }, []);

  return (
    <main>
      <p>Backend connection: {connectionState}</p>
    </main>
  );
}

export default App;