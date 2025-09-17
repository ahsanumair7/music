import asyncio
import json
import os
from src.agent.capability import MatchingCapability
from src.main import AgentWorker
from src.agent.capability_worker import CapabilityWorker
import requests


class MusicCapability(MatchingCapability):
    worker: AgentWorker = None
    capability_worker: CapabilityWorker = None

    @classmethod
    def register_capability(cls) -> "MatchingCapability":
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
        ) as file:
            data = json.load(file)
        return cls(
            unique_name=data["unique_name"],
            matching_hotwords=data["matching_hotwords"],
        )

    async def play_audio(self):
        """
        Play Music by downloading directly from python requests Module and passing the content to play_audio function
        """
        music_response = requests.get("https://cdn.pixabay.com/download/audio/2023/10/22/audio_6d1fc2e6c3.mp3?filename=rise-up-172724.mp3")
        music = music_response.content
        await self.capability_worker.play_audio(music)

        """
        Play Music by directly from the ability folder 
        You can click on choose file and upload the file to the ability workspace
        """
        await self.capability_worker.play_from_audio_file("song.mp3")

        # Resume the normal workflow
        self.capability_worker.resume_normal_flow()

    def call(self, worker: AgentWorker):
        # Initialize the worker and capability worker
        self.worker = worker
        self.capability_worker = CapabilityWorker(self.worker)

        # Start the advisor functionality
        self.worker.session_tasks.create(self.play_audio())
