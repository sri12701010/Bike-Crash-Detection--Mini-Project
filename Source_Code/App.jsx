import { useEffect, useMemo, useRef, useState } from "react";
import AlertCard from "./components/AlertCard";
import BikeConnection from "./components/BikeConnection";
import Dashboard from "./components/Dashboard";
import RecentEvents from "./components/RecentEvents";
import SensorForm from "./components/SensorForm";
import { getRecentSensorData, predictCrash, sendAlert, uploadSensorData } from "./api";

export default function App() {
  const [mode, setMode] = useState("manual");
  const [prediction, setPrediction] = useState(null);
  const [alert, setAlert] = useState(null);
  const [recentEvents, setRecentEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const processingRef = useRef(false);

  const riskBand = useMemo(() => {
    if (!prediction) return "No reading yet";
    if (prediction.is_crash) return "Critical";
    if (prediction.crash_probability >= 0.45) return "Elevated";
    return "Normal";
  }, [prediction]);

  useEffect(() => {
    let mounted = true;
    const refreshRecent = async () => {
      try {
        const response = await getRecentSensorData(8);
        if (mounted) {
          setRecentEvents(response.data.items || []);
        }
      } catch {
        // Keep UI usable even if recent endpoint is temporarily unavailable.
      }
    };

    refreshRecent();
    const timer = setInterval(refreshRecent, 5000);
    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, []);

  const processSensorPayload = async (payload, source = "manual") => {
    if (processingRef.current) {
      return;
    }

    processingRef.current = true;
    setLoading(true);
    setError("");

    try {
      await uploadSensorData(payload);
      const predictionResponse = await predictCrash(payload);
      const predictionData = predictionResponse.data;

      setPrediction(predictionData);
      setRecentEvents((prev) => [{ ...payload, source, sample_id: crypto.randomUUID() }, ...prev].slice(0, 8));

      if (predictionData.is_crash) {
        const alertResponse = await sendAlert({
          latitude: payload.latitude,
          longitude: payload.longitude,
          contact: "+1234567890",
          note: "Crash detected from frontend flow",
        });
        setAlert(alertResponse.data);
      } else {
        setAlert(null);
      }
    } catch (err) {
      setError(err?.response?.data?.detail || "Request failed. Is backend running?");
    } finally {
      processingRef.current = false;
      setLoading(false);
    }
  };

  const onManualSubmit = async (payload) => {
    await processSensorPayload(payload, "manual");
  };

  const onBikeData = async (payload) => {
    await processSensorPayload(payload, "bike");
  };

  return (
    <main className="app-shell">
      <header className="hero">
        <p className="eyebrow">Bike Safety Intelligence</p>
        <h1>Bike Crash Detection Control Room</h1>
        <p>
          Simulate live sensor telemetry, evaluate crash risk, and trigger alerts with location context in
          real time.
        </p>
      </header>

      {error ? <p className="error">{error}</p> : null}

      <section className="card mode-card">
        <h2>Data Input Mode</h2>
        <div className="mode-switch">
          <button
            type="button"
            className={mode === "manual" ? "mode active" : "mode"}
            onClick={() => setMode("manual")}
          >
            Manual Entry
          </button>
          <button
            type="button"
            className={mode === "bike" ? "mode active" : "mode"}
            onClick={() => setMode("bike")}
          >
            Connect Bike
          </button>
        </div>
        <p className="muted">
          Manual Entry works without any hardware. Connect Bike supports live sensor packets from Bluetooth-enabled devices.
        </p>
      </section>

      <section className="layout-grid">
        <div>
          <Dashboard prediction={prediction} riskBand={riskBand} />
          {mode === "manual" ? (
            <SensorForm onSubmit={onManualSubmit} loading={loading} />
          ) : (
            <BikeConnection onBikeData={onBikeData} loading={loading} />
          )}
        </div>
        <div>
          <AlertCard alert={alert} prediction={prediction} />
          <RecentEvents events={recentEvents} />
        </div>
      </section>
    </main>
  );
}
