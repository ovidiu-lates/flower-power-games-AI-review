import { Gamepad2 } from "lucide-react";
import { useState } from "react";

interface GameArtworkProps {
  src: string;
  name: string;
}

export default function GameArtwork({ src, name }: GameArtworkProps) {
  const [failed, setFailed] = useState(false);

  if (failed || !src) {
    return <div className="artwork-fallback" role="img" aria-label={`${name} cover unavailable`}><Gamepad2 /><strong>{name}</strong></div>;
  }

  return <img src={src} alt={`${name} cover`} onError={() => setFailed(true)} />;
}