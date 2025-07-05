import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { XCircle } from "lucide-react";

const formSchema = z
  .object({
    emailContent: z.string().optional(),
    emailFile: z.any().optional(),
  })
  .refine(
    (data) =>
      data.emailContent || (data.emailFile && data.emailFile.length > 0),
    {
      message: "É necessário fornecer o conteúdo do e-mail ou um arquivo.",
      path: ["emailContent"],
    },
  );

type EmailFormValues = z.infer<typeof formSchema>;

interface EmailFormProps {
  onSubmit: (data: { content: string | File }) => void;
  isLoading: boolean;
}

const EmailForm: React.FC<EmailFormProps> = ({ onSubmit, isLoading }) => {
  const form = useForm<EmailFormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      emailContent: "",
      emailFile: undefined,
    },
  });

  const watchedEmailFile = form.watch("emailFile");
  const fileSelected = watchedEmailFile && watchedEmailFile.length > 0;

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      form.setValue("emailFile", files);
      form.clearErrors("emailContent");
    } else {
      form.setValue("emailFile", undefined);
    }
  };

  const handleClearFile = () => {
    form.setValue("emailFile", undefined);

    const fileInput = document.getElementById("emailFile") as HTMLInputElement;
    if (fileInput) {
      fileInput.value = "";
    }
  };

  const handleTextareaChange = (
    event: React.ChangeEvent<HTMLTextAreaElement>,
  ) => {
    const text = event.target.value;
    form.setValue("emailContent", text);
    if (text.trim() !== "") {
      form.clearErrors("emailContent");
    }
  };

  const handleSubmit = async (values: EmailFormValues) => {
    if (values.emailFile && values.emailFile.length > 0) {
      onSubmit({ content: values.emailFile[0] });
    } else if (values.emailContent) {
      onSubmit({ content: values.emailContent });
    }
  };

  return (
    <Card className="w-full max-w-2xl bg-card text-card-foreground p-8 rounded-xl shadow-lg">
      <CardHeader>
        <CardTitle className="text-center text-primary">
          Analisar E-mail
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className="space-y-6"
          >
            <FormField
              control={form.control}
              name="emailContent"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Conteúdo do E-mail</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Cole o conteúdo do e-mail aqui..."
                      className="min-h-[150px] rounded-lg shadow-sm focus-visible:ring-autou-azul-escuro"
                      {...field}
                      value={field.value || ""}
                      onChange={handleTextareaChange}
                      disabled={fileSelected || isLoading}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="relative flex items-center justify-center my-4">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-border" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">Ou</span>
              </div>
            </div>

            <FormField
              control={form.control}
              name="emailFile"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Upload de Arquivo (.txt, .pdf)</FormLabel>
                  <FormControl>
                    <div className="relative">
                      <Input
                        id="emailFile"
                        type="file"
                        accept=".txt,.pdf"
                        className="rounded-lg shadow-sm focus-visible:ring-autou-azul-escuro pr-10"
                        onChange={handleFileChange}
                        disabled={!!form.watch("emailContent") || isLoading}
                      />
                      {fileSelected && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={handleClearFile}
                          className="absolute right-1 top-1/2 -translate-y-1/2 p-1 h-auto rounded-full text-muted-foreground hover:text-foreground"
                          disabled={isLoading}
                        >
                          <XCircle className="h-5 w-5" />
                        </Button>
                      )}
                    </div>
                  </FormControl>
                  {fileSelected && (
                    <p className="text-sm text-muted-foreground mt-1">
                      Arquivo selecionado: {watchedEmailFile[0]?.name}
                    </p>
                  )}
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button
              type="submit"
              className="w-full rounded-lg shadow-md hover:shadow-lg transition-all duration-200 bg-primary text-primary-foreground hover:bg-primary/90"
              disabled={isLoading}
            >
              {isLoading ? "Analisando..." : "Analisar E-mail"}
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default EmailForm;
