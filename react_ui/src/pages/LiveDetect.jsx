import { useEffect } from "react";
import { liveDetect } from "../services/api";

function LiveDetect() {
  useEffect(() => {
    const timer = setInterval(async () => {
      const res = await liveDetect();
      if (res.data.severity === "CRITICAL") {
        alert(`🚨 CRITICAL ATTACK from ${res.data.src_ip}`);
      }
    }, 3000);

    return () => clearInterval(timer);
  }, []);

  return <h2>Live Detection Running...</h2>;
}

export default LiveDetect;
