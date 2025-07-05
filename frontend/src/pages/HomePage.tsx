// frontend/src/pages/HomePage.tsx

import React, { useState } from "react";
import EmailForm from "../components/EmailForm";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Separator } from "../components/ui/separator";
import {
  AlertDialog,
  AlertDialogTitle,
  AlertDialogAction,
  AlertDialogFooter,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogHeader,
} from "../components/ui/alert-dialog";
import type { EmailProcessingResult } from "../backend_types";

const HomePage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<EmailProcessingResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showErrorDialog, setShowErrorDialog] = useState(false);
  const handleSubmitEmail = async (data: { content: string | File }) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    if (typeof data.content === "string") {
      formData.append("email_content", data.content);
    } else {
      formData.append("email_file", data.content);
    }

    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/process-email",
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || "Erro desconhecido ao processar o e-mail.",
        );
      }

      const result: EmailProcessingResult = await response.json();
      setResults(result);
    } catch (err) {
      console.error("Erro ao enviar e-mail para o backend:", err);
      setError(err instanceof Error ? err.message : String(err));
      setShowErrorDialog(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-4 sm:p-6 md:p-8">
      <Card className="w-full max-w-2xl bg-card text-card-foreground p-4 sm:p-6 md:p-8 rounded-xl shadow-lg">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold text-primary mb-2">
            Classificador de E-mails AutoU
          </CardTitle>
          <p className="text-muted-foreground">
            Analise seus e-mails e obtenha classificações e respostas
            automáticas.
          </p>
        </CardHeader>
        <CardContent>
          <EmailForm onSubmit={handleSubmitEmail} isLoading={isLoading} />

          {isLoading && (
            <div className="mt-8 text-center text-primary animate-pulse">
              <p>Analisando e-mail...</p>
              <p className="text-sm text-muted-foreground">
                Isso pode levar alguns segundos.
              </p>
            </div>
          )}

          {results && (
            <div className="mt-8">
              <h2 className="text-2xl font-semibold text-primary mb-4 text-center">
                Resultados da Análise
              </h2>
              <Separator className="mb-4 bg-border" /> {/* Separador visual */}
              <div className="space-y-4">
                <div>
                  <p className="text-lg font-medium text-foreground">
                    Classificação:
                  </p>
                  <p
                    className={`text-xl font-bold ${results.classification === "Produtivo" ? "text-autou-azul-escuro" : "text-autou-amarelo-dourado"} transition-colors duration-300`}
                  >
                    {results.classification}
                  </p>
                </div>
                <div>
                  <p className="text-lg font-medium text-foreground">
                    Resposta Sugerida:
                  </p>
                  <p className="text-muted-foreground text-base leading-relaxed bg-muted p-4 rounded-lg shadow-inner transition-all duration-300">
                    {results.suggested_response}
                  </p>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* AlertDialog para exibir erros */}
      <AlertDialog open={showErrorDialog} onOpenChange={setShowErrorDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="text-destructive">
              Erro ao Processar E-mail
            </AlertDialogTitle>
            <AlertDialogDescription>{error}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogAction onClick={() => setShowErrorDialog(false)}>
              Entendi
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default HomePage;
