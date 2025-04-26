import axios from "./axiosClient";

export async function uploadPhoto(fileUri: string, token: string) {
  const form = new FormData();
  form.append("file", {
    uri: fileUri,
    name: `${Date.now()}.jpg`,
    type: "image/jpeg",
  } as any);

  const resp = await axios.post("/photos/upload", form, {
    headers: {
      "Content-Type": "multipart/form-data",
      Authorization: `Bearer ${token}`,
    },
  });
  return resp.data as { fotoId: number; usuarios_detectados: number[] };
}

