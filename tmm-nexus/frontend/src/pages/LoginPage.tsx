import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { useAuth } from "../hooks/useAuth";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(email, password);
      navigate("/dashboard");
    } catch {
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-brand-cream px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <img src={logo} alt="The Mac Media" className="mx-auto h-16 w-auto" />
          <h1 className="mt-4 text-2xl font-semibold text-gray-900">TMM Nexus</h1>
          <p className="mt-1 text-sm text-gray-500">Sign in to your workspace</p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
        >
          <div className="space-y-4">
            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>

          {error && <p className="mt-4 text-sm text-red-600">{error}</p>}

          <Button type="submit" loading={loading} className="mt-6 w-full">
            Sign in
          </Button>
        </form>
      </div>
    </div>
  );
}
